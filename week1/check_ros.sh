#!/bin/bash

echo "# ROS2 환경 점검 ($(date +%F))"
echo "- ROS_DISTRO: ${ROS_DISTRO:-미설정}"
echo "- ROS_DOMAIN_ID: ${ROS_DOMAIN_ID:-0(기본값)}"
echo "- ros2 명령: $(command -v ros2 || echo 없음)"
echo "- 설치 패키지 수: $(ros2 pkg list 2>/dev/null | wc -l)"

ros2 doctor --report 2>/dev/null | grep -A2 "NETWORK" | head -5
# 김범열 바보
