# python_monitoring
## 파이썬 사이드프로젝트 - 프로세스 모니터

가상환경 구축순서
1. ```python -m venv .venv```로 가상환경 디렉토리 준비
2. ```source .venv/bin/activate```로 경로 설정 및 가성환경 활성화
3. ```.venv/bin/python -m pip install -r requirements.txt```로 가상환경에 의존성 추가
4. 가상환경에서 실행
5. 작업 완료후 ```deactivate```로 가상환경 비활성

### pyinstaller
클라이언트 디렉토리로 이동후 진행
- 일반환경
```
pyinstaller --onefile --name ProcessMonitor main.py 
```
- 실제 
```
~/ProcessMonitor/.venv/bin/pyinstaller --name ProcessMonitor --onefile --noconsole main.py
```