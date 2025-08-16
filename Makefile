.PHONY: mvn

pull-jars:
	mvn dependency:copy-dependencies -DoutputDirectory=${PWD}/jars_1