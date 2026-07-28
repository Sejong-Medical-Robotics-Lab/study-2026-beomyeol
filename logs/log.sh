#!/bin/bash

# 오늘 날짜의 학습일지 파일 경로
F="logs/$(date +%F).md"

# logs 폴더가 없으면 생성
mkdir -p logs

# 오늘 날짜의 파일이 없을 때만 기본 양식 생성
if [ ! -f "$F" ]; then
    printf "# 학습일지 %s\n\n## 오늘 배운 것\n\n## 막힌 것\n\n" "$(date +%F)" > "$F"
fi

# 생성된 학습일지 열기
nano "$F"