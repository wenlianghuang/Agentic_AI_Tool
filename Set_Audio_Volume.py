import ctypes
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import argparse
# 設定音量常數
SPEAKER_VOLUME = 0.10  # 系統喇叭音量設為30%
APP_VOLUME = 0.15  # 應用程式音量設為100%

def set_master_volume(speaker_volume):
    speaker_volume = round(speaker_volume / 100, 2)
    """將系統主喇叭音量設定為30%"""
    try:
        # 獲取喇叭設備
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
        
        # 獲取當前音量
        current_volume = volume.GetMasterVolumeLevelScalar()
        
        # 設置喇叭音量為30%
        #volume.SetMasterVolumeLevelScalar(SPEAKER_VOLUME, None)
        volume.SetMasterVolumeLevelScalar(speaker_volume, None)
        print(f"已將系統喇叭音量從 {current_volume*100:.1f}% 調整為 {speaker_volume*100:.1f}%")
        #return True
    except Exception as e:
        print(f"設置系統喇叭音量時發生錯誤: {e}")
        #return False

def set_all_app_volumes(app_audio_volume):
    print(f"正在將所有應用程式音量調整為 {app_audio_volume}%...")
    app_audio_volume = round(app_audio_volume / 100, 2)
    # 獲取所有音訊會話
    sessions = AudioUtilities.GetAllSessions()
    adjusted_count = 0
    
    for session in sessions:
        try:
            # 獲取音量接口
            app_volume = session.SimpleAudioVolume
            
            # 獲取應用名稱
            if session.Process:
                app_name = session.Process.name()
            else:
                app_name = "系統音效"
            
            # 將應用程式音量設置為100%
            app_volume.SetMasterVolume(app_audio_volume, None)
            adjusted_count += 1
            
            print(f"{app_name}: 音量已調整為 {app_audio_volume*100:.1f}%")
        except:
            pass
    
    print(f"已調整 {adjusted_count} 個應用程式的音量為 {app_audio_volume * 100:.1f}%")

def show_current_volumes():
    """顯示所有音訊源的當前音量"""
    print("\n當前音量設置:")
    print("-" * 30)
    
    # 顯示系統喇叭音量
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
    master_volume = volume.GetMasterVolumeLevelScalar()
    
    print(f"系統喇叭: {master_volume*100:.1f}%")
    
    # 顯示應用程式音量
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        try:
            if session.SimpleAudioVolume and session.Process:
                current_volume = session.SimpleAudioVolume.GetMasterVolume()
                print(f"{session.Process.name()}: {current_volume*100:.1f}%")
        except:
            pass
    
    print("-" * 30)
def adjust_volume(master_volume, app_volume):
    """調整系統和應用程式音量"""
    try:
        set_master_volume(master_volume)
    except Exception as e:
        print(f"設置系統音量時發生錯誤: {e}")
    try:
        set_all_app_volumes(app_volume)
    except Exception as e:
        print(f"設置應用程式音量時發生錯誤: {e}")
if __name__ == "__main__":
    
    '''
    try:
        print("Windows 音量統一調整工具")
        print("正在調整音量...")
        
        # 調整系統喇叭音量
        set_master_volume()
        
        # 調整所有應用程式音量
        set_all_app_volumes()
        
        # 顯示最終設置
        show_current_volumes()
        
        print("\n音量調整已完成！按任意鍵退出...")
        input()
    except Exception as e:
        print(f"\n發生錯誤: {e}")
        input("按任意鍵退出...")
    '''
    parser = argparse.ArgumentParser(description="Open camera and microphone, record video and audio.")
    parser.add_argument("--master-volume", type=float, default=30, help="Set the master volume level (0 to 100)")
    parser.add_argument("--app-volume", type=float, default=30, help="Set the application volume level (0 to 100)")
    args = parser.parse_args()
    # 調整系統和應用程式音量
    adjust_volume(args.master_volume, args.app_volume)
