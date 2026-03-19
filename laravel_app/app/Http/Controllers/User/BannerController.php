<?php

namespace App\Http\Controllers\User;

use App\Http\Controllers\Controller;
use App\Models\BannerDetail;
use App\Models\Banner;
use App\Jobs\CreateBannersJob;
use App\Models\Model;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Storage;
class BannerController extends Controller
{
    public function createBanners(Request $request)
    {
        try {
            $validated = $request->validate([
                'description' => 'required|string|max:2500',
                'width' => 'required|integer|min:320|max:1536',
                'height' => 'required|integer|min:320|max:1536',
                'number' => 'required|integer|min:1|max:4',
            ]);
            // Lưu BannerDetail
            $bannerDetail = BannerDetail::create([
                'user_id' => Auth::user()->id,
                'description' => $validated['description'],
                'width' => $validated['width'],
                'height' => $validated['height'],
                'number' => $validated['number'],
            ]);
            // Load api key
            $google_api_key = Model::findOrFail(1);
            $openrouter_xai_api_key = Model::findOrFail(2);
            $openai_api_key = Model::findOrFail(3);
            // Chuẩn bị dữ liệu cho job
            $data = [
                'google_api_key' => $google_api_key,
                'openrouter_xai_api_key' => $openrouter_xai_api_key,
                'openai_api_key' => $openai_api_key,
                'width' => $validated['width'],
                'height' => $validated['height'],
                'number' => $validated['number'],
                'user_request' => $validated['description'],
            ];
            $jobId = uniqid(); 
            // Gửi job
            CreateBannersJob::dispatch($data, $bannerDetail->id, $jobId, Auth::user()->id);
            return back()->with('success', 'Đã gửi yêu cầu')->withInput();
        } catch (\Exception $e) {
            Log::error('Lỗi khi tạo BannerDetail: ' . $e->getMessage());
            return back()->with('error', 'Lỗi xử lý yêu cầu: ' . $e->getMessage());
        }
    }


    public function deleteBannerDetail($bannerDetailsId)
    {
        try {
            $bannerDetail = BannerDetail::findOrFail($bannerDetailsId);

            // Xóa các file ảnh trong storage trước khi xóa banners
            foreach ($bannerDetail->banners as $banner) {
                if ($banner->link_banner && str_starts_with($banner->link_banner, '/storage/banners/')) {
                    $path = str_replace('/storage/', '', $banner->link_banner); // chuyển sang path trong disk
                    Storage::disk('public')->delete($path);
                }
            }
            // Xóa tất cả banners liên quan
            $bannerDetail->banners()->delete();
            // Xóa banner detail
            $bannerDetail->delete();
            return back()->with('success', 'BannerDetail và các Banner liên quan đã được xóa thành công');
        } catch (\Exception $e) {
            return back()->with('error', 'Không tìm thấy hoặc lỗi khi xóa');
        }
    }


    public function deleteBanner($bannerId)
    {
        try {
            $banner = Banner::findOrFail($bannerId);

            // Xóa các file ảnh trong storage trước khi xóa banners
            if ($banner->link_banner && str_starts_with($banner->link_banner, '/storage/banners/')) {
                $path = str_replace('/storage/', '', $banner->link_banner); // chuyển sang path trong disk
                Storage::disk('public')->delete($path);
            }
            // Xóa banner 
            $banner->delete();
            return back()->with('success', 'Banner liên quan đã được xóa thành công');
        } catch (\Exception $e) {
            return back()->with('error', 'Không tìm thấy hoặc lỗi khi xóa');
        }
    }


    public function saveBanner(Request $request)
    {
        try {
            // Xác thực dữ liệu
            $request->validate([
                'image' => 'required|string', // Dữ liệu base64
                'banner_details_id' => 'required|exists:banner_details,id' // Kiểm tra banner_details_id
            ]);

            // Giải mã base64
            $imageData = $request->input('image');
            $imageData = str_replace('data:image/png;base64,', '', $imageData);
            $imageData = str_replace(' ', '+', $imageData);
            $imageContent = base64_decode($imageData);

            // Tạo tên tệp duy nhất
            $fileName = 'banner_' . $request->banner_details_id . '_' . time() . '.png';
            $path = 'banners/' . $fileName;

            // Lưu ảnh vào storage
            Storage::disk('public')->put($path, $imageContent);

            // Cập nhật hoặc tạo bản ghi trong bảng banners
            $banner = Banner::updateOrCreate([
                'banner_details_id' => $request->banner_details_id,
                'link_banner' => Storage::url("banners/{$fileName}"),
            ]);

            return response()->json([
                'success' => true,
                'message' => 'Ảnh banner đã được lưu thành công!',
            ]);
        } catch (\Exception $e) {
            return response()->json([
                'success' => false,
                'message' => 'Lỗi khi lưu ảnh: ' . $e->getMessage()
            ], 500);
        }
    }

    public function publishBanner(Request $request, $id)
    {
        $banner = Banner::findOrFail($id);
        if ($request->isMethod('put')) {
            // Công khai banner
            $banner->is_published = true;
            $banner->published_at = now();
        } elseif ($request->isMethod('delete')) {
            // Hủy công khai banner
            $banner->is_published = false;
            $banner->published_at = null;
        }
        $banner->save();
        return redirect()->back()->with('success', 'Cập nhật trạng thái thành công!');
    }
}