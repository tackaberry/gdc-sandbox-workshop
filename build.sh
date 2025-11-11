#!/bin/bash

source .env
source functions.sh

case "$1" in
    app)
        docker_build "./workloads/app/" "web-server-test"
        ;;
    translate)
        docker_build "./workloads/translate/" "translate"
        ;;
    open)
        docker_build "./workloads/open/ollama/" "ollama"
        docker_pull "ghcr.io/open-webui/open-webui:main" "open-webui"
        ;;
    elastic)
        docker_pull "elasticsearch:8.11.4" "elasticsearch"
        docker_pull "kibana:8.11.4" "kibana"
        docker_pull "busybox:latest" "busybox"
        ;;
    video)
        docker_build "./workloads/video/app/" "video-intelligence"
        ;;        
    *)
        # if $1 and $2 are not empty, run docker_build with those parameters
        if [ -n "$1" ] && [ -n "$2" ]; then
            docker_build "$1" "$2"
            exit 0
        fi
        echo "Usage: $0 {app|translate|open|elastic} or ./workloads/path/ image-name"
        exit 1
        ;;
esac
