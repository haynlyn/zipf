.PHONY : all clean settings help

include config.mk

DATA=$(wildcard data/*.txt)
RESULTS=$(patsubst data/%.txt,results/%.csv,$(DATA))

## all : regenerate all results.
all : results/collated.png

## results/collated.png : plot the collated results.
results/collated.png : results/collated.csv $(PLOTPARAMS)
	python $(PLOT) $< --outfile $@ --plotparams $(word 2,$^)

## results/collated.csv : collate all results.
results/collated.csv : $(RESULTS) $(COLLATE)
	@mkdir -p results
	python $(COLLATE) $(RESULTS) > $@

## results/%.csv : regenerate results for any book.
results/%.csv : data/%.txt $(COUNT) $(SUMMARY)
	@bash $(SUMMARY) $< Title
	@bash $(SUMMARY) $< Author
	python $(COUNT)  $< > $@

## test-saveconfig : save plot configurations
test-saveconfig : $(PLOT)
	python $(PLOT) results/collated.csv --outfile results/collated.png \
		--saveconfig

## results : regenerate results for all books
results : $(RESULTS)

## clean : remove all generated files.
clean :
	rm $(RESULTS) results/collated.csv results/collated.png

## settings : show variables' values.
settings:
	@echo COUNT: $(COUNT)
	@echo DATA : $(DATA)
	@echo RESULTS: $(RESULTS)
	@echo COLLATE: $(COLLATE)
	@echo PLOT: $(PLOT)
	@echo SUMMARY: $(SUMMARY)

## help : show this message.
help :
	@grep -h -E '^##' ${MAKEFILE_LIST} | sed -e 's/## //g' \
		| column -t -s ':'
