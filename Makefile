clean:
	rm -f waterapputils/*.pyc
	rm -f waterapputils/*.txt
	rm -f waterapputils/*.xml
	rm -r data/watertxt-datafiles/waterapputils-watertxt/*
	rm -r data/waterxml-datafiles/waterapputils-waterxml/*
	rm -r data/water-batch-run-datafiles/sample-batch-run-output/waterapputils-batchrun-info/
	rm -r data/water-batch-run-datafiles/sample-batch-run-output/014*/waterapputils*
	rm -r data/water-batch-run-datafiles/sample-batch-run-output/waterapputils-ecoflow/
	rm -r data/water-batch-run-datafiles/sample-batch-run-output/waterapputils-oasis/
	rm -f tests/*.pyc
	rm -f tests/*.txt
	rm -r tests/test-dir
	rm -f tests/*.csv

