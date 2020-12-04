#!/bin/bash
ROOT_DIR=`jq '.root_directory' settings.json`
echo $ROOT_DIR
PSW=`jq '.database_password' settings.json`
echo $PSW
