import subprocess
import sys
import os

def run_streamlit():
    try:
        # Streamlit 앱 실행
        subprocess.run([
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "app/streamlit_app.py",
            "--server.port=8501"
        ])
    except KeyboardInterrupt:
        print("\nStreamlit 앱이 종료되었습니다.")
    except Exception as e:
        print(f"오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    run_streamlit() 