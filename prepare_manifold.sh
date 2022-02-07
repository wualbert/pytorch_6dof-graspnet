#!/usr/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
target_dir="$SCRIPT_DIR"/simplified
echo "Saving results to $target_dir"
mkdir -p "$SCRIPT_DIR"/simplified
for file in $(find $1 -type f -print) #"$1"/*
do
    echo "Preparing $file"
    tmp_file="$target_dir"/temp.watertight.obj
    echo "....Saving watertight temp file to $tmp_file"
    manifold "$file" "$tmp_file" -s
    final_file="$target_dir"/"$file"
    # hacky way to ensure directory exists
    mkdir -p "$final_file"
    rm -r "$final_file"
    echo "....Saving simplified result to $final_file"
    simplify -i "$tmp_file" -o "$final_file" -m -r 0.02
    # Convert to stl
    final_filename="${final_file%.*}"
    ctmconv "$final_file" "$final_filename.stl"
    rm "$final_file"
done
rm "$tmp_file"