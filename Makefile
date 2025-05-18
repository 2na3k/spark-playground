.PHONY: mvn

pull-jars:
	mvn dependency:copy-dependencies -DoutputDirectory=./jars_1