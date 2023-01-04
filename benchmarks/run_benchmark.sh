kernprof -l ./bench.py
python -m line_profiler ./bench.py.lprof

# Clean up
rm ./bench.py.lprof