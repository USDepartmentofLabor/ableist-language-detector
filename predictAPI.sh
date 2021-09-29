#!/bin/bash

# Usage example:
# curl http://localhost:1234/invocations \
#   -H 'Content-Type: application/json; format=pandas-records' \
#   -d '{"data":["
#   requirements
#       - must be able to move your hands repeatedly
#       - type on a computer
#       - comfortable with lifting heavy boxes
#       - excellent communication skills
#       - move your wrists in circles and bend your arms"]}'

# To pipe from stdin:
curl http://localhost:1234/invocations \
-H "Content-Type: application/json; format=pandas-records" \
--data-binary {\"data\":[\""$(</dev/stdin)"\"]}
