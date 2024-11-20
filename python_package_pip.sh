#!/bin/bash
# pip 최신버전으로 업그레이드 진행
echo "Upgrading pip to the latest version..."
pip install --upgrade pip

# 패키지 설치 시작
echo "Installing required Python packages..."
pip install -y aiofiles==24.1.0 aiohappyeyeballs==2.4.3 aiohttp==3.11.0 aiomysql==0.2.0 aiosignal==1.3.1 annotated-types==0.7.0 anyio==4.6.2.post1 attrs==24.2.0 certifi==2024.8.30 cffi==1.17.1 charset-normalizer==3.4.0 contourpy==1.3.1 cryptography==43.0.3 cycler==0.12.1 DateTime==5.5 Deprecated==1.2.14 distro==1.9.0 fonttools==4.54.1 frozenlist==1.5.0 h11==0.14.0 httpcore==1.0.7 httpx==0.27.2 idna==3.10 jiter==0.7.1 kiwisolver==1.4.7 matplotlib==3.9.2 msgpack==1.1.0 multidict==6.1.0 multipledispatch==1.0.0 numpy==2.1.3 openai==0.28.0 packaging==24.2 pandas==2.2.3 pillow==11.0.0 ping3==4.0.8 propcache==0.2.0 py-cord==2.6.1 pycparser==2.22 pydantic==2.9.2 pydantic_core==2.23.4 PyMySQL==1.1.1 pyparsing==3.2.0 python-dateutil==2.9.0.post0 python-dotenv==1.0.1 pytz==2024.2 requests==2.32.3 setuptools==75.5.0 six==1.16.0 sniffio==1.3.1 tqdm==4.67.0 typing_extensions==4.12.2 tzdata==2024.2 urllib3==2.2.3 wrapt==1.16.0 xlrd==2.0.1 yarl==1.17.1 zope.interface==7.1.1

# 모든 패키지를 최신 버전으로 업그레이드
echo "Upgrading all packages to the latest version..."
pip install --upgrade $(pip list --outdated | awk '{if(NR>2)print $1}')

echo "All packages and pip have been upgraded to the latest versions!"

echo "All packages installed successfully!"
