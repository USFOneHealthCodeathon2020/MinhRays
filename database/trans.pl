#!/usr/bin/perl
open(csv,"MaxQuant_data.csv");
open(p,">demo.fasta");
$title=<csv>;
while ($read=<csv>) {
	chomp($read);
	@reads=split(/\,/,$read);
	@id=split(/ /,$reads[$#reads]);
	print p ">$id[0]_$id[1]_$id[2]-$reads[16]\n$reads[0]\n";
}