import os
import cv2

# 定义六个视频文件路径
video_paths = ['D01_20220714.avi', 'D02_20220714.avi', 'D03_20220714.avi',
                'D04_20220714.avi', 'D05_20220714.avi', 'D06_20220714.avi']
file_paths = 'G:/Download/NetdiskBaidu/download/Vofsurgery/video'
video_path_all= [os.path.join(file_paths,video) for video in video_paths]

# 截图保存目录
save_dir = 'screenshots'
for i in range(1,7):
    ppath = os.path.join('screenshots',str(i))
    # re file
    if not os.path.exists(ppath):
        os.makedirs(ppath)
    else:
        for filename in os.listdir(ppath):
            file_path = os.path.join(ppath, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'删除 {file_path} 失败. 原因: {e}')

for i in range(1,7):
    ppath = os.path.join('screenshots',str(i))                
    video_path = video_path_all[i-1]
    cap = cv2.VideoCapture(video_path)
    # 检查视频是否打开成功
    if not cap.isOpened():
        print("Error opening video file.")
    else:
        frame_count = 0
        saved_count = 0
    while True:
        # 读取视频中的一帧
        ret, frame = cap.read()
        # 检查帧是否正确读取
        if not ret:
            break
        # 每隔24帧进行一次截图
        if frame_count % 24 == 0:
            save_path = os.path.join(ppath, f'len{i}_screenshot_{saved_count:04d}.jpg')
            cv2.imwrite(save_path, frame)
            print(f'Saved: {save_path}')
            saved_count += 1
        frame_count += 1

    # 释放视频捕捉器
    cap.release()
    print(f"Done processing video{i}.")

# 结束

# # 存储每个视频的帧计数器
# frame_counts = [0] * len(video_paths)

# while True:
#     # 读取每个视频的当前帧
#     frames = [cap.read()[1] for cap in caps]
 
#     # 更新帧计数器
#     frame_counts = [frame_counts[i] + 1 if frame is not None else frame_counts[i] for i, frame in enumerate(frames)]

#     # 检查是否有帧读取失败
#     if any(frame is None for frame in frames):
#         print("某个视频文件已结束或读取帧失败。")
#         break





#     # 显示每个视频帧和当前帧编号
#     for i, frame in enumerate(frames):
#         if frame is not None:
#             # 在帧上添加文本显示帧编号
#             cv2.putText(frame, f'Frame: {frame_counts[i]}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
#             cv2.imshow(f'Video Channel {i+1}', frame)

#     # 按 'q' 键退出
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # 释放所有视频捕捉对象
# for cap in caps:
#     cap.release()

# # 关闭所有OpenCV窗口
# cv2.destroyAllWindows()
