FROM ubuntu:20.04

RUN apt-get update && apt-get install --yes python3.9
RUN apt-get update && apt-get install --yes python3-pip
RUN apt-get update && apt-get install --yes openjdk-16-jre-headless

RUN apt-get update && apt-get install --yes time
RUN apt-get update && apt-get install --yes wget
RUN apt-get clean

WORKDIR /tmp

# install clingo
RUN wget https://github.com/potassco/clingo/releases/download/v5.4.0/clingo-5.4.0-linux-x86_64.tar.gz \
    && tar -zxf clingo-5.4.0-linux-x86_64.tar.gz clingo-5.4.0-linux-x86_64/clingo \
    && mkdir /tools \
    && cp ./clingo-5.4.0-linux-x86_64/clingo /tools

# install plasp
RUN wget https://github.com/potassco/plasp/releases/download/v3.1.1/plasp-3.1.1-linux-x86_64.tar.gz \
    && tar -zxf plasp-3.1.1-linux-x86_64.tar.gz plasp-3.1.1/plasp \
    && cp ./plasp-3.1.1/plasp /tools

WORKDIR /tools
# download ASP encoding used in the paper 
# L.Chrpa, W. Faber, D. Fiser, and M. Morak,
# "Determining action reversibility in STRIPS using answer set programming",
# In International Conference on Logic Programming 2020 (ICLP 2020),
# [Online]. Available: http://ceur-ws.org/Vol-2678/paper2.pdf
# Benchmark files found here: https://seafile.aau.at/d/e0aedc92b4c546d5bf9a/
RUN wget --trust-server-names --referer https://seafile.aau.at/d/e0aedc92b4c546d5bf9a/files/?p=/ \ 
    'https://seafile.aau.at/d/e0aedc92b4c546d5bf9a/files/?p=/sequential-horizon.uurev.sat.lp&dl=1'
# For ASPQ encoding, see
# https://seafile.aau.at/d/eb22aab5223f4e8abfcc/
RUN wget --trust-server-names --referer https://seafile.aau.at/d/eb22aab5223f4e8abfcc/files/?p=/ \ 
    'https://seafile.aau.at/d/eb22aab5223f4e8abfcc/files/?p=/qasp-0.1.2.jar&dl=1'
RUN wget --trust-server-names --referer https://seafile.aau.at/d/eb22aab5223f4e8abfcc/files/?p=/ \ 
    'https://seafile.aau.at/d/eb22aab5223f4e8abfcc/files/?p=/run-pddl-horizon.py&dl=1'
# For QSP/ESLP encoding, see
# https://seafile.aau.at/d/cd4cb0d65d124a619920/
RUN wget --trust-server-names --referer https://seafile.aau.at/d/cd4cb0d65d124a619920/files/?p=/ \ 
    'https://seafile.aau.at/d/cd4cb0d65d124a619920/files/?p=/sequential-horizon.general.asp&dl=1'


# download action.py and PDDL.py from github.com/pucrs-automated-planning/pddl-parser
RUN wget https://raw.githubusercontent.com/pucrs-automated-planning/pddl-parser/581a0905b2cf3f481d84df56ac65fbb52902eddf/action.py
RUN wget https://raw.githubusercontent.com/pucrs-automated-planning/pddl-parser/581a0905b2cf3f481d84df56ac65fbb52902eddf/PDDL.py

# install Python dependencies
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

ENV PATH="/tools:${PATH}"

VOLUME [ "/reversibility" ]
WORKDIR /reversibility