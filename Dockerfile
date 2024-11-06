FROM ubuntu:latest
LABEL authors="ivan.berestianyi"

ENTRYPOINT ["top", "-b"]