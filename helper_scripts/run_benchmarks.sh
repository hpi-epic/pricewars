#!/usr/bin/env bash

declare map=(
    [abc,0]=1
    [abc,1]=2
    [abc,2]=3
    [abc,3]=4
    [def,0]="http://..."
    [def,1]=33
    [def,2]=2
)
key="def"
i=1
echo "${map[$key,$i]}"   # => 33
i=0
echo "${map[$key,$i]}"   # => 33

