#!/bin/zsh
ab -n 1000 -c 80 -p student.json -T  application/json  -H "Authorization: Bearer test" -r https://api.onekana.naconek.ke/api/v1/students/