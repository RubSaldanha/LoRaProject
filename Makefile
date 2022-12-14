all:
	@(if [ ! -d build ]; then mkdir build; fi; cd build;\
	  if [ ! -d snr_bin]; then mkdir snr_bin; fi; cmake ..; make)

clean:
	rm -rf build /snr_bin
	rm -rf build /CMakeCache.txt
