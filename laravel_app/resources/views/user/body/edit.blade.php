<!DOCTYPE html>
<html lang="vi">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Banner Blitz - {{ $title }}</title>
    <!-- Favicons -->
    <link href="{{ asset($favicon ?? 'assets/images/favicon.png') }}" rel="icon">
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome cho biểu tượng -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&family=Open+Sans:wght@400;700&family=Lora:wght@400;700&family=Montserrat:wght@400;700&family=Playfair+Display:wght@400;700&family=Poppins:wght@400;700&family=Raleway:wght@400;700&family=Source+Sans+Pro:wght@400;700&family=Inter:wght@400;700&family=Noto+Sans:wght@400;700&family=Arial&family=Helvetica&family=Times+New+Roman&family=Courier+New&family=Verdana&family=Georgia&family=Tahoma&family=Trebuchet+MS&family=Arial+Narrow&family=Book+Antiqua&family=Century+Gothic&family=Comic+Sans+MS&family=Garamond&family=Palatino+Linotype&display=swap" rel="stylesheet">
    <!-- Fabric.js -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/fabric.js/5.3.1/fabric.min.js"></script>
    <!-- Thêm CSRF token -->
    <meta name="csrf-token" content="{{ csrf_token() }}">
    <!-- SweetAlert2 -->
    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>

    <style>
        body {
            background: #3e3e3e;
            margin: 0;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
            overflow: hidden;
        }

        .overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            z-index: 1;
        }

        .image-container {
            position: relative;
            z-index: 2;
            border-radius: 10px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            max-width: 100%;
            max-height: 80vh;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .image-container canvas {
            width: 100%;
            height: auto;
            max-height: 60vh;
            border-radius: 5px;
            cursor: move;
            z-index: 3;
        }

        .toolbar {
            position: absolute;
            bottom: 10px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(0, 0, 0, 0.8);
            border-radius: 20px;
            padding: 10px 20px;
            display: flex;
            align-items: center;
            gap: 15px;
            z-index: 4;
        }

        .toolbar .btn {
            background: none;
            border: none;
            color: white;
            display: flex;
            align-items: center;
            gap: 5px;
            font-size: 14px;
        }

        .toolbar .btn i {
            font-size: 16px;
        }

        .text-toolbar {
            position: fixed;
            left: 0;
            top: 50%;
            transform: translateY(-50%);
            background: #fff;
            border-radius: 0 10px 10px 0;
            padding: 15px;
            display: none;
            flex-direction: column;
            gap: 10px;
            width: 250px;
            z-index: 5;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }

        .text-toolbar .close-btn {
            background: #e0e0e0;
            border: none;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            align-self: flex-end;
        }

        .text-toolbar .add-text-btn {
            background: linear-gradient(45deg, #ff6f61, #ff9f43);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 12px;
            font-size: 16px;
            font-weight: 600;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            width: 100%;
            box-shadow: 0 4px 15px rgba(255, 111, 97, 0.4);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .text-toolbar .add-text-btn:hover {
            background: linear-gradient(45deg, #ff9f43, #ff6f61);
            box-shadow: 0 6px 20px rgba(255, 111, 97, 0.6);
            transform: translateY(-2px);
        }

        .text-toolbar .add-text-btn:active {
            transform: translateY(1px);
            box-shadow: 0 2px 10px rgba(255, 111, 97, 0.3);
        }

        .text-toolbar .add-text-btn i {
            font-size: 18px;
        }

        .text-toolbar .search-section {
            position: relative;
        }

        .search-section input {
            width: 100%;
            padding: 8px 30px 8px 30px;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
        }

        .search-section i {
            position: absolute;
            left: 10px;
            top: 50%;
            transform: translateY(-50%);
            color: #6c757d;
        }

        .text-toolbar .font-list {
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 10px;
            height: 300px;
            overflow-y: auto;
        }

        .font-list div {
            padding: 8px;
            font-size: 14px;
            cursor: pointer;
            border-radius: 5px;
        }

        .font-list div:hover {
            background: #e0e0e0;
        }

        .font-list div.selected {
            background: #007bff;
            color: white;
            font-weight: bold;
        }

        .text-toolbar .font-section-label {
            font-size: 14px;
            font-weight: bold;
            margin-bottom: 5px;
        }

        .text-toolbar .color-section {
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .color-section label {
            font-size: 14px;
        }

        .color-section input[type="color"] {
            border: none;
            width: 30px;
            height: 30px;
            padding: 0;
            cursor: pointer;
        }

        .text-toolbar .style-buttons {
            display: flex;
            gap: 10px;
        }

        .style-buttons button {
            flex: 1;
            background: #e0e0e0;
            border: none;
            border-radius: 8px;
            padding: 8px;
            font-size: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .style-buttons button.active {
            background: #007bff;
            color: white;
        }

        .delete-btn {
            position: absolute;
            top: -15px;
            right: -15px;
            background: #ff4444;
            color: white;
            border: none;
            border-radius: 50%;
            width: 25px;
            height: 25px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 12px;
            z-index: 10;
        }

        @media (max-width: 400px) {
            .text-toolbar {
                width: 180px;
                left: 0px;
            }

            .font-list {
                height: 200px;
            }
        }

        @media (max-width: 576px) {
            .toolbar {
                padding: 8px 15px;
                gap: 10px;
            }

            .toolbar .btn i {
                font-size: 14px;
            }

            .text-toolbar {
                width: 150px;
                padding: 8px;
                font-size: 14px;
            }

            .font-list {
                height: 240px;
            }

            .text-toolbar .add-text-btn {
                padding: 10px;
                font-size: 14px;
            }

            .text-toolbar .add-text-btn i {
                font-size: 16px;
            }
        }

        @media (max-width: 768px) {
            .image-container {
                width: 100vw;
                /* Lấp đầy chiều rộng màn hình */
                max-width: 100%;
                /* Đảm bảo không vượt quá viewport */
                height: auto;
                /* Chiều cao tự động điều chỉnh theo nội dung */
                max-height: 90vh;
                /* Giới hạn chiều cao tối đa */
                margin: 0 auto;
                /* Căn giữa */
            }

            .image-container canvas {
                width: 100%;
                /* Lấp đầy chiều rộng container */
                height: auto;
                /* Chiều cao tự động theo tỷ lệ */
                max-height: 80vh;
                /* Tăng nhẹ để hiển thị nhiều nội dung hơn */
                display: block;
                /* Đảm bảo canvas không bị ảnh hưởng bởi margin */
            }

            .toolbar {
                bottom: 5px;
                padding: 5px 10px;
            }

            .text-toolbar {
                width: 200px;
                /* Giảm chiều rộng trên di động */
                padding: 10px;
                /* Giảm padding */
                gap: 8px;
                /* Giảm khoảng cách giữa các phần tử */
                border-radius: 0 8px 8px 0;
                /* Giảm bo góc */
            }
        }
    </style>
</head>

<body>
    <!-- Lớp phủ nền mờ đục -->
    <div class="overlay"></div>
    <!-- Container chính -->
    <div class="image-container">
        <!-- Canvas để hiển thị ảnh và văn bản -->
        <canvas id="canvas"></canvas>
        <!-- Thanh công cụ chỉnh sửa văn bản -->
        <div class="text-toolbar" id="textToolbar">
            <button class="close-btn" id="closeTextToolbar" title="Đóng">
                <i class="fas fa-chevron-left"></i>
            </button>
            <div class="search-section">
                <i class="fas fa-search"></i>
                <input type="text" id="fontSearch" placeholder="Tìm kiếm phông chữ">
            </div>
            <button class="add-text-btn" id="addTextBtn" title="Thêm ô văn bản">
                <i class="fas fa-text-height"></i> Thêm ô văn bản
            </button>
            <div class="font-section-label">Phông chữ</div>
            <div class="font-list" id="fontList">
                <div data-font="Roboto" style="font-family: 'Roboto', sans-serif;">Roboto</div>
                <div data-font="Open Sans" style="font-family: 'Open Sans', sans-serif;">Open Sans</div>
                <div data-font="Lora" style="font-family: 'Lora', serif;">Lora</div>
                <div data-font="Montserrat" style="font-family: 'Montserrat', sans-serif;">Montserrat</div>
                <div data-font="Playfair Display" style="font-family: 'Playfair Display', serif;">Playfair Display</div>
                <div data-font="Poppins" style="font-family: 'Poppins', sans-serif;">Poppins</div>
                <div data-font="Raleway" style="font-family: 'Raleway', sans-serif;">Raleway</div>
                <div data-font="Source Sans Pro" style="font-family: 'Source Sans Pro', sans-serif;">Source Sans Pro</div>
                <div data-font="Inter" style="font-family: 'Inter', sans-serif;">Inter</div>
                <div data-font="Noto Sans" style="font-family: 'Noto Sans', sans-serif;">Noto Sans</div>
                <div data-font="Arial" style="font-family: 'Arial', sans-serif;">Arial</div>
                <div data-font="Helvetica" style="font-family: 'Helvetica', sans-serif;">Helvetica</div>
                <div data-font="Times New Roman" style="font-family: 'Times New Roman', serif;">Times New Roman</div>
                <div data-font="Courier New" style="font-family: 'Courier New', monospace;">Courier New</div>
                <div data-font="Verdana" style="font-family: 'Verdana', sans-serif;">Verdana</div>
                <div data-font="Georgia" style="font-family: 'Georgia', serif;">Georgia</div>
                <div data-font="Tahoma" style="font-family: 'Tahoma', sans-serif;">Tahoma</div>
                <div data-font="Trebuchet MS" style="font-family: 'Trebuchet MS', sans-serif;">Trebuchet MS</div>
                <div data-font="Arial Narrow" style="font-family: 'Arial Narrow', sans-serif;">Arial Narrow</div>
                <div data-font="Book Antiqua" style="font-family: 'Book Antiqua', serif;">Book Antiqua</div>
                <div data-font="Century Gothic" style="font-family: 'Century Gothic', sans-serif;">Century Gothic</div>
                <div data-font="Comic Sans MS" style="font-family: 'Comic Sans MS', sans-serif;">Comic Sans MS</div>
                <div data-font="Garamond" style="font-family: 'Garamond', serif;">Garamond</div>
                <div data-font="Palatino Linotype" style="font-family: 'Palatino Linotype', serif;">Palatino Linotype</div>
            </div>
            <div class="color-section">
                <label>Chọn màu chữ</label>
                <input type="color" class="form-control-color rounded-circle" id="textColorPicker" value="#000000">
            </div>
            <div class="style-buttons">
                <button id="boldBtn" title="Đậm">
                    <i class="fas fa-bold"></i>
                </button>
                <button id="italicBtn" title="Nghiêng">
                    <i class="fas fa-italic"></i>
                </button>
            </div>
        </div>

        <!-- Thanh công cụ chính -->
        <div class="toolbar" id="toolbar">
            <button class="btn" id="textBtn" title="Thêm văn bản">
                <i class="fas fa-text-height"></i>
            </button>
            <button class="btn" id="uploadImageBtn" title="Tải ảnh lên">
                <i class="fas fa-images"></i>
            </button>
            <button class="btn" id="saveBtn" title="Lưu ảnh" data-banner-details-id="{{ $banner->banner_details_id }}">
                <i class="fas fa-save"></i>
            </button>
            <button class="btn" id="downloadBtn" title="Tải xuống">
                <i class="fas fa-download"></i>
            </button>
            <a href="{{ route('load_view_create_banners') }}" class="btn" title="Đóng">
                <i class="fas fa-close"></i>
            </a>
        </div>
    </div>

    <!-- Input ẩn để tải ảnh -->
    <input type="file" id="imageUpload" accept="image/*" style="display: none;">

    <!-- Bootstrap JS và Popper.js -->
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.8/dist/umd/popper.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.min.js"></script>
    <script>
        // Khởi tạo Fabric.js canvas
        const canvas = new fabric.Canvas('canvas', {
            width: 600,
            height: 400,
            selection: true
        });

        // Tải ảnh nền mặc định
        const imgUrl = "{{ asset($banner->link_banner) }}";
        fabric.Image.fromURL(imgUrl, function(img) {
            if (!img) {
                console.error('Không thể tải ảnh');
                alert('Lỗi: Không thể tải ảnh. Vui lòng kiểm tra lại URL.');
                return;
            }

            function resizeCanvas() {
                const maxWidth = window.innerWidth * 0.9; // 90% chiều rộng cửa sổ
                const maxHeight = window.innerHeight * 0.6; // 60% chiều cao cửa sổ
                const scale = Math.min(maxWidth / img.width, maxHeight / img.height);

                img.scale(scale);
                img.set({
                    selectable: false,
                    evented: false
                });

                canvas.setWidth(img.width * scale);
                canvas.setHeight(img.height * scale);
                canvas.setBackgroundImage(img, canvas.renderAll.bind(canvas));
            }

            // Gọi hàm resize ban đầu
            resizeCanvas();

            // Thêm sự kiện resize để cập nhật khi cửa sổ thay đổi kích thước
            window.addEventListener('resize', resizeCanvas);
        }, {
            crossOrigin: 'anonymous'
        }, function(err) {
            console.error('Lỗi tải ảnh:', err);
            alert('Lỗi: Không thể tải ảnh. Vui lòng thử lại.');
        });

        // Xử lý tải ảnh lên
        const uploadImageBtn = document.getElementById('uploadImageBtn');
        const imageUpload = document.getElementById('imageUpload');

        uploadImageBtn.addEventListener('click', () => {
            imageUpload.click();
        });

        imageUpload.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(event) {
                    fabric.Image.fromURL(event.target.result, function(img) {
                        img.scaleToWidth(canvas.getWidth() / 4); // Kích thước ban đầu bằng 1/4 chiều rộng canvas
                        img.set({
                            left: canvas.getWidth() / 2,
                            top: canvas.getHeight() / 2,
                            originX: 'center',
                            originY: 'center',
                            selectable: true,
                            hasControls: true,
                            hasBorders: true,
                            lockUniScaling: false,
                            evented: true
                        });
                        canvas.add(img);
                        canvas.setActiveObject(img);
                        canvas.renderAll();
                    }, {
                        crossOrigin: 'anonymous'
                    });
                };
                reader.readAsDataURL(file);
                imageUpload.value = ''; // Reset input để cho phép chọn lại cùng file
            }
        });

        // Xử lý xóa ảnh hoặc văn bản khi chọn
        canvas.on('selection:created', function(e) {
            const activeObject = e.selected[0];
            if (activeObject && (activeObject.type === 'image' || activeObject.type === 'i-text')) {
                // Thêm nút xóa
                const deleteBtn = document.createElement('button');
                deleteBtn.className = 'delete-btn';
                deleteBtn.innerHTML = '<i class="fas fa-trash"></i>';
                deleteBtn.onclick = function() {
                    canvas.remove(activeObject);
                    canvas.renderAll();
                    deleteBtn.remove();
                };
                document.querySelector('.image-container').appendChild(deleteBtn);

                // Cập nhật vị trí nút xóa theo đối tượng
                function updateDeleteBtnPosition() {
                    const zoom = canvas.getZoom();
                    const boundingRect = activeObject.getBoundingRect(true);
                    deleteBtn.style.left = `${boundingRect.left + boundingRect.width + 10}px`;
                    deleteBtn.style.top = `${boundingRect.top - 15}px`;
                }

                updateDeleteBtnPosition();
                canvas.on('object:modified', updateDeleteBtnPosition);
                canvas.on('object:scaling', updateDeleteBtnPosition);
                canvas.on('object:moving', updateDeleteBtnPosition);
                canvas.on('object:rotating', updateDeleteBtnPosition);

                // Xóa nút khi bỏ chọn
                canvas.on('selection:cleared', function() {
                    deleteBtn.remove();
                    canvas.off('object:modified', updateDeleteBtnPosition);
                    canvas.off('object:scaling', updateDeleteBtnPosition);
                    canvas.off('object:moving', updateDeleteBtnPosition);
                    canvas.off('object:rotating', updateDeleteBtnPosition);
                });
            }
        });

        // Xử lý lưu ảnh
        const saveBtn = document.getElementById('saveBtn');
        saveBtn.addEventListener('click', function() {
            const dataURL = canvas.toDataURL({
                format: 'png',
                quality: 1
            });
            const bannerDetailsId = saveBtn.getAttribute('data-banner-details-id');
            // Gửi ảnh qua AJAX
            fetch('/user/save-banner', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]').content
                    },
                    body: JSON.stringify({
                        image: dataURL,
                        banner_details_id: bannerDetailsId
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        Swal.fire({
                            icon: 'success',
                            title: 'Thành công',
                            text: 'Ảnh đã được lưu thành công!',
                            timer: 2000,
                            showConfirmButton: false
                        });
                    } else {
                        Swal.fire({
                            icon: 'error',
                            title: 'Lỗi',
                            text: data.message || 'Đã xảy ra lỗi không xác định',
                            timer: 3000,
                            showConfirmButton: true
                        });
                    }
                })
                .catch(error => {
                    console.error('Lỗi:', error);
                    console.log('Đã xảy ra lỗi khi lưu ảnh.');
                });
        });

        // Tải lại trạng thái canvas (nếu cần)
        function loadCanvasState() {
            const savedState = localStorage.getItem('canvasState');
            if (savedState) {
                canvas.loadFromJSON(savedState, canvas.renderAll.bind(canvas), function(o, object) {
                    if (object.type === 'image') {
                        object.set({
                            selectable: true,
                            hasControls: true,
                            hasBorders: true,
                            lockUniScaling: false,
                            evented: true
                        });
                    } else if (object.type === 'i-text') {
                        object.set({
                            editable: true,
                            selectable: true,
                            hasControls: true,
                            hasBorders: true,
                            lockRotation: false,
                            lockUniScaling: false,
                            lockMovementX: false,
                            lockMovementY: false,
                            lockScalingX: false,
                            lockScalingY: false,
                            evented: true
                        });
                    }
                });
            }
        }

        // Tải trạng thái khi khởi động (tùy chọn)
        // loadCanvasState();

        // Xử lý tải xuống ảnh
        const downloadBtn = document.getElementById('downloadBtn');
        downloadBtn.addEventListener('click', function() {
            const dataURL = canvas.toDataURL({
                format: 'png',
                quality: 1
            });
            const link = document.createElement('a');
            link.href = dataURL;
            link.download = 'edited_image.png';
            link.click();
        });

        // Xử lý thanh công cụ văn bản
        const toolbar = document.getElementById('toolbar');
        const textBtn = document.getElementById('textBtn');
        const textToolbar = document.getElementById('textToolbar');
        const addTextBtn = document.getElementById('addTextBtn');
        const closeTextToolbar = document.getElementById('closeTextToolbar');
        const fontSearch = document.getElementById('fontSearch');
        const fontList = document.getElementById('fontList');
        const textColorPicker = document.getElementById('textColorPicker');
        const boldBtn = document.getElementById('boldBtn');
        const italicBtn = document.getElementById('italicBtn');

        // Mở/đóng text-toolbar
        textBtn.addEventListener('click', function() {
            textToolbar.style.display = textToolbar.style.display === 'flex' ? 'none' : 'flex';
            toolbar.style.display = 'none';
        });

        closeTextToolbar.addEventListener('click', function() {
            textToolbar.style.display = 'none';
            toolbar.style.display = 'flex';
        });

        // Xử lý tìm kiếm phông chữ
        let selectedFont = 'Roboto';
        let selectedColor = textColorPicker.value;
        let isBold = false;
        let isItalic = false;

        let allFonts = Array.from(fontList.querySelectorAll('div')).map(item => ({
            element: item,
            font: item.getAttribute('data-font'),
            text: item.textContent
        }));

        fontSearch.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            allFonts.forEach(font => {
                if (font.text.toLowerCase().includes(searchTerm)) {
                    font.element.style.display = 'block';
                } else {
                    font.element.style.display = 'none';
                }
            });
        });

        // Xử lý chọn phông chữ
        function clearSelection() {
            fontList.querySelectorAll('div').forEach(item => {
                item.classList.remove('selected');
            });
        }

        function loadFont(fontName) {
            const link = document.createElement('link');
            link.href = `https://fonts.googleapis.com/css2?family=${fontName.replace(' ', '+')}&display=swap`;
            link.rel = 'stylesheet';
            document.head.appendChild(link);
        }

        fontList.querySelectorAll('div').forEach(item => {
            item.addEventListener('click', function() {
                clearSelection();
                this.classList.add('selected');
                selectedFont = this.getAttribute('data-font');
                loadFont(selectedFont);
                const activeObject = canvas.getActiveObject();
                if (activeObject && activeObject.type === 'i-text') {
                    activeObject.set('fontFamily', selectedFont);
                    canvas.renderAll();
                }
            });
        });

        // Xử lý chọn màu chữ
        textColorPicker.addEventListener('input', function() {
            selectedColor = this.value;
            const activeObject = canvas.getActiveObject();
            if (activeObject && activeObject.type === 'i-text') {
                activeObject.set('fill', selectedColor);
                canvas.renderAll();
            }
        });

        // Xử lý nút đậm (bold)
        boldBtn.addEventListener('click', function() {
            isBold = !isBold;
            this.classList.toggle('active', isBold);
            const activeObject = canvas.getActiveObject();
            if (activeObject && activeObject.type === 'i-text') {
                activeObject.set('fontWeight', isBold ? 'bold' : 'normal');
                canvas.renderAll();
            }
        });

        // Xử lý nút nghiêng (italic)
        italicBtn.addEventListener('click', function() {
            isItalic = !isItalic;
            this.classList.toggle('active', isItalic);
            const activeObject = canvas.getActiveObject();
            if (activeObject && activeObject.type === 'i-text') {
                activeObject.set('fontStyle', isItalic ? 'italic' : 'normal');
                canvas.renderAll();
            }
        });

        // Xử lý nút "Thêm ô văn bản"
        addTextBtn.addEventListener('click', function() {
            const text = new fabric.IText('Nhập văn bản', {
                left: canvas.getWidth() / 2,
                top: canvas.getHeight() / 2,
                fontFamily: selectedFont,
                fontSize: 20,
                fill: selectedColor,
                fontWeight: isBold ? 'bold' : 'normal',
                fontStyle: isItalic ? 'italic' : 'normal',
                editable: true,
                originX: 'center',
                originY: 'center',
                hasControls: true,
                hasBorders: true,
                lockRotation: false,
                lockUniScaling: false,
                lockMovementX: false,
                lockMovementY: false,
                lockScalingX: false,
                lockScalingY: false,
                evented: true,
                selectable: true
            });
            canvas.add(text);
            canvas.setActiveObject(text);
            canvas.renderAll();
        });

        // Chỉ cho phép chỉnh sửa khi nhấp đúp
        canvas.on('mouse:dblclick', function(options) {
            const target = options.target;
            if (target && target.type === 'i-text') {
                canvas.setActiveObject(target);
                target.enterEditing();
                target.selectAll();
            }
        });

        // Đảm bảo canvas luôn có thể tương tác
        canvas.on('object:modified', function() {
            canvas.renderAll();
        });
    </script>
</body>

</html>