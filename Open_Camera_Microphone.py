import cv2
import pyaudio
import wave
#from moviepy.editor import VideoFileClip, AudioFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
import argparse
import os
# Open camera and microphone
def open_camera_and_microphone(final_output_filename):
    # Camera setup
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        return

    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30  # Default to 30 FPS if not available
    video_filename = "output.avi"
    #final_output_filename = final_output_filename
    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(video_filename, fourcc, fps, (frame_width, frame_height))

    # Microphone setup
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 1
    rate = 44100
    audio_filename = "output.wav"

    p = pyaudio.PyAudio()
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    print("Recording...")
    frames = []

    try:
        while True:
            # Read camera frame
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            cv2.imshow('Camera', frame)

            # Write video frame to file
            out.write(frame)

            # Read microphone audio
            data = stream.read(chunk, exception_on_overflow=False)
            frames.append(data)

            # Exit on 'q' key press
            if cv2.waitKey(1) == ord('q'):
                break
    finally:
        # Release camera
        cap.release()
        out.release()
        cv2.destroyAllWindows()

        # Stop and close microphone stream
        stream.stop_stream()
        stream.close()
        p.terminate()

        # Save audio to file
        wf = wave.open(audio_filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
        wf.close()

        print(f"Video saved to {video_filename}, audio saved to {audio_filename}")

        # Combine video and audio into a single file
        print("Combining video and audio...")
        video_clip = VideoFileClip(video_filename)
        audio_clip = AudioFileClip(audio_filename)
        #final_clip = video_clip.set_audio(audio_clip)
        final_clip = video_clip.with_audio(audio_clip)
        final_clip.write_videofile(final_output_filename, codec="libx264", audio_codec="aac",logger=None)

        video_clip.close()
        audio_clip.close()
        final_clip.close()
        print(f"Final video with audio saved to {final_output_filename}")
        # Remove temporary video and audio files
        try:
            #shutil.rmtree(video_filename, ignore_errors=True)
            #shutil.rmtree(audio_filename, ignore_errors=True)
            os.remove(video_filename)
            os.remove(audio_filename)
            print("Temporary files removed.")
        except Exception as e:
            print(f"Error while deleting temporary files: {e}")
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Open camera and microphone, record video and audio.")
    parser.add_argument("--output", type=str, default="output_with_audio.mp4", help="Final output filename with audio")
    args = parser.parse_args()
    open_camera_and_microphone(args.output)