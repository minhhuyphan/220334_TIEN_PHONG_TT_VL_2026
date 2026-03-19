<?php

namespace App\Jobs;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Storage;
use App\Models\Banner;
use App\Models\BannerDetail;
use Illuminate\Support\Facades\Auth;
use App\Events\BannerJobCompleted;

class CreateBannersJob implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    protected $data;
    protected $bannerDetailsId;
    public $jobId;
    public $userId;

    public function __construct($data, $bannerDetailsId, $jobId, $userId)
    {
        $this->data = $data;
        $this->bannerDetailsId = $bannerDetailsId;
        $this->jobId = $jobId;
        $this->userId = $userId;
    }


    public function handle()
    {
        $apiUrl = config('services.fastapi.url');
        $apiKey = config('services.fastapi.api_key');
        Log::info('Data gửi tới FastAPI:', $this->data);
        $status = 'success';    // default
        $errorMessage = null;

        try {
            $response = Http::withHeaders([
                'API-Key' => $apiKey,
            ])->timeout(1200)->asForm()->post($apiUrl, $this->data);

            if ($response->successful()) {
                $bannerUrls = $response->json();

                if (!is_array($bannerUrls)) {
                    Log::error('Dữ liệu FastAPI không hợp lệ: ' . json_encode($response->json()));
                    $status = 'failed';
                    $errorMessage = 'Dữ liệu FastAPI không hợp lệ';
                } else {
                    foreach ($bannerUrls as $index => $url) {
                        try {
                            $imageContent = Http::timeout(10)->get($url)->body();
                            $filename = "banner_{$this->bannerDetailsId}_{$index}.png";
                            Storage::disk('public')->put("banners/{$filename}", $imageContent);

                            $localUrl = Storage::url("banners/{$filename}");
                            Banner::create([
                                'banner_details_id' => $this->bannerDetailsId,
                                'link_banner' => $localUrl,
                            ]);
                        } catch (\Exception $e) {
                            Log::error("Lỗi tải ảnh {$url}: {$e->getMessage()}");
                            // Tiếp tục với URL gốc nếu lỗi
                            Banner::create([
                                'banner_details_id' => $this->bannerDetailsId,
                                'link_banner' => $url,
                            ]);
                        }
                    }

                    Log::info('Đã lưu ' . $this->data['number'] . ' banner cho banner_detail ID: ' . $this->bannerDetailsId);
                }
            } else {
                Log::error('Lỗi FastAPI: ' . $response->status() . ' - ' . $response->body());
                $status = 'failed';
                $errorMessage = 'Lỗi FastAPI: ' . $response->body();
            }
        } catch (\Exception $e) {
            Log::error('Lỗi khi gọi FastAPI: ' . $e->getMessage());
            $status = 'failed';
            $errorMessage = 'Lỗi khi gọi FastAPI: ' . $e->getMessage();
        }


        // Cập nhật trạng thái banner.
        try {
            $bannerDetail = BannerDetail::findOrFail($this->bannerDetailsId);
            if ($status === 'success') {
                $bannerDetail->status = 1;
                $bannerDetail->save();
                Log::info("BannerDetail {$this->bannerDetailsId} hoàn tất.");
            } else {
                $bannerDetail->status = -1;
                $bannerDetail->save();
                Log::error("Job thất bại cho BannerDetail {$this->bannerDetailsId}. Lỗi: {$errorMessage}");
            }
        } catch (\Exception $e) {
            Log::error("Lỗi trong BannerJobController: {$e->getMessage()}");
        }

        // Gọi event.
        event(new BannerJobCompleted($this->userId));
    }
}