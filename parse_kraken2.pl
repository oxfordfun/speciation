#!/usr/bin/perl

use strict;
use warnings;

# REQUIREMENTS
if ( (!(defined($ARGV[0]))) or (!(defined($ARGV[1]))) or (!(defined($ARGV[2]))) or (!(defined($ARGV[3]))) )
	{ print "\n\nThis script will parse a Kraken output file to report (a) the dominant family/genus/species in the sample, and (b) all other species also present.\n";
	  print "We require a min. coverage of x% of the total reads AND a min. number of reads PER SPECIES. Set these to 0 to report everything.\n";
	  print "USAGE:\tperl parse_kraken_report.pl [path to Kraken report] [path to output file; must end .json] [min. species coverage, as %] [min. species coverage, as no. of reads]\n";
	  print "E.G.:\tperl parse_kraken_report.pl report.tab out.txt 1 10000\n\n\n";
	  exit 1;
	}
my $in_file = $ARGV[0]; my $out_file = $ARGV[1]; my $pct_threshold = $ARGV[2]; my $num_threshold = $ARGV[3];
if (!(-e($in_file)))
	{ die "ERROR: cannot find $in_file\n"; }
if ( (-e($in_file)) and (!(-s($in_file))) )
	{ die "ERROR: $in_file is empty\n"; }
if ($out_file !~ /^(.*?)\.json$/)
	{ die "ERROR: output file $out_file must end with suffix .json\n"; }
if ($pct_threshold !~ /^\d+\.?\d*$/)
	{ die "ERROR: $pct_threshold is not a positive number\n"; }
if ($num_threshold !~ /^\d+$/)
	{ die "ERROR: $num_threshold is not a positive integer\n"; }
if ($pct_threshold > 100)
	{ die "ERROR: $pct_threshold is a % and cannot be > 100\n"; }

# READ KRAKEN REPORT
# the Kraken report is assumed to be the standard format: 6 tab-delimited columns, with one line per taxon. This is described at https://github.com/DerrickWood/kraken2/wiki/Manual#output-formats. We will confirm this as we parse.
my @S = (); my @G = (); my @G1 = (); my @F = ();
open(IN,'<',$in_file) or die $!;
while(<IN>)
	{ my $line = $_; chomp($line);
	  my @line = split(/\t/,$line);
	  next if ($#line != 5); # in a correctly formatted Kraken report, each row will have 6 columns; we will skip those that don't
	  my $pc_frags 		   = $line[0]; # percentage of fragments covered by the clade rooted at this taxon. NOTE: for this purpose, 'fragment' is synonymous with 'read'.
	  my $num_frags_rooted = $line[1]; # number of fragments covered by the clade rooted at this taxon, i.e. all fragments at this taxonomic level AND LOWER
	  my $num_frags_direct = $line[2]; # number of fragments assigned directly to this taxon
	  my $rank_code 	   = $line[3]; # rank code, indicating (U)nclassified, (R)oot, (D)omain, (K)ingdom, (P)hylum, (C)lass, (O)rder, (F)amily, (G)enus, or (S)pecies. Takes the form of one letter, optionally followed by one number.
	  my $ncbi_taxon_id    = $line[4]; # NCBI taxonomic ID number
	  my $name 			   = $line[5]; # scientific name
	  $pc_frags =~ s/^\s+//; $name =~ s/^\s+//;
	  next if (($pc_frags 		  < $pct_threshold) and ($name ne 'Homo sapiens')); # skip classifications not supported by a min % of fragments
	  next if (($num_frags_rooted < $num_threshold) and ($name ne 'Homo sapiens')); # skip classifications not supported by a min no. of fragments
	  if (($pc_frags =~ /^\d+\.?\d*$/) and ($num_frags_rooted =~ /^\d+$/) and ($num_frags_direct =~ /^\d+$/) and ($rank_code =~ /^\w{1}\d*$/) and ($ncbi_taxon_id =~ /^\d+$/) and ($name =~ /\w+/))
		{ if 	($rank_code eq 'S') { push(@S,[$num_frags_rooted,$pc_frags,$name]); }
		  elsif ($rank_code eq 'G') { push(@G,[$num_frags_rooted,$pc_frags,$name]); }
		  elsif ($rank_code eq 'F') { push(@F,[$num_frags_rooted,$pc_frags,$name]); }
		  if (($name =~ /^Mycobact.*?$/) and ($rank_code eq 'G1')) # Kraken does not resolve classifications among the Mycobacteriaceae as well as Mykrobe. At best, it can detect species complexes. We shall retain these classifications to look at later, as they may indicate whether this is a mixed-mycobacterial sample.
			{ push(@G1,[$num_frags_rooted,$pc_frags,$name]); }
		}
	  else
		{ die "ERROR: malformatted Kraken report, at line $. (\"$line\")\n"; }
	}
close(IN) or die $!;
if ($#S == -1) { die "ERROR: no species classifications meet thresholds of > $num_threshold reads and > $pct_threshold % of total reads\n"; }
if ($#G == -1) { die "ERROR: no genus classifications meet thresholds of > $num_threshold reads and > $pct_threshold % of total reads\n";   }
if ($#F == -1) { die "ERROR: no family classifications meet thresholds of > $num_threshold reads and > $pct_threshold % of total reads\n";  }
my @sorted_F = map { $_->[0] } sort { $b->[1] <=> $a->[1] } map { [$_, $_->[0]] } @F;
my @sorted_G = map { $_->[0] } sort { $b->[1] <=> $a->[1] } map { [$_, $_->[0]] } @G;
my @sorted_S = map { $_->[0] } sort { $b->[1] <=> $a->[1] } map { [$_, $_->[0]] } @S;

# CREATE OUTPUT FILE, REPORTING "DOMINANT SPECIES" AND "OTHER SPECIES"
open(OUT,'>',$out_file) or die $!;
print OUT "\{\n\n";
my $is_mycobact = 0; my $top_species_printed = 0; my $top_species = '';
if ($sorted_F[0][2] eq 'Mycobacteriaceae') # Kraken cannot adequately resolve classifications among the Mycobacteriaceae. If this represents the dominant family, SP3 will defer classification to Mykrobe instead. In this case, we must assume the top genus and species hits are also within the Mycobacteriaceae and do not continue to report Kraken's findings here - their % values will not be as accurate as Mykrobe.
	{ print OUT "\tFamily: \{\n\t\tname: \"$sorted_F[0][2]\",\n\t\treads: \"$sorted_F[0][1]\",\n\t\tpercentage\: \"$sorted_F[0][0]\",\n\t\tnotes\:\"for higher-resolution classification, see Mykrobe report\"\n\t\t\}\n";
	  $is_mycobact++;
	}
else
	{ print OUT "\tFamily: \{\n\t\tname: \"$sorted_F[0][2]\",\n\t\treads: \"$sorted_F[0][1]\",\n\t\tpercentage\: \"$sorted_F[0][0]\",\n\t\tnotes\:\"\"\n\t\t\}\n";
	  print OUT "\tGenus: \{\n\t\tname: \"$sorted_G[0][2]\",\n\t\treads: \"$sorted_G[0][1]\",\n\t\tpercentage\: \"$sorted_G[0][0]\",\n\t\tnotes\:\"\"\n\t\t\}\n";
	  print OUT "\tSpecies (major): \{\n\t\tname: \"$sorted_S[0][2]\",\n\t\treads: \"$sorted_S[0][1]\",\n\t\tpercentage\: \"$sorted_S[0][0]\",\n\t\tnotes\:\"\"\n\t\t\}\n";
	  $top_species = $sorted_S[0][2]; $top_species_printed++;
	}
print OUT "\tSpecies (minor):[\n";
my $other_than_human_found = 0;
for(my $x=0;$x<@sorted_S;$x++)
	{ next if (($top_species_printed > 0) and ($sorted_S[$x][2] eq $top_species));
	  next if (($is_mycobact > 0) and ($sorted_S[$x][2] =~ /^Mycobact.*?$/)); # if the top family hit is Mycobacteriaceae, we ignore all subsequent species-level classifications as they will not be accurate. However, what of mixed Mycobacteriaceae?
	  print OUT "\t\t\{\n\t\tname: \"$sorted_S[$x][2]\",\n\t\treads: \"$sorted_S[$x][1]\",\n\t\tpercentage\: \"$sorted_S[$x][0]\",\n\t\tnotes\:\"possible contaminant\"\n\t\t\},\n";
	  $other_than_human_found++ unless ($sorted_S[$x][2] eq 'Homo sapiens');
	}
print OUT "\t]\n";
print OUT "\tThresholds: \{\n\t\treads: \"$num_threshold\",\n\t\tpercentage: \"$pct_threshold\"\n\t\t\}\n";

# IF THE TOP FAMILY HIT IS MYCOBACTERIACEAE, WE DEFER TO THE MYKROBE REPORT FOR HIGHER-RESOLUTION CLASSIFICATION. AS SUCH, WE DO NOT OUTPUT SPECIFIC MYCOBACTERIAL GENUS OR SPECIES CLASSIFICATIONS.
# HOWEVER, THIS MAY CAUSE US TO OVERLOOK MIXED-MYCOBACTERIAL SAMPLES, WHICH KRAKEN COULD OTHERWISE DETECT. WE WILL NOW CHECK WHETHER THIS IS THE CASE AND IF SO, REPORT A FINAL WARNING.
if ($is_mycobact > 0)
	{ my @sorted_G1 = map { $_->[0] } sort { $b->[1] <=> $a->[1] } map { [$_, $_->[0]] } @G1;
	  my $num_G1 = @sorted_G1;
	  if ($num_G1 > 1)
		{ print OUT "\tSpecies complex:[\n";
		  for(my $x=0;$x<@sorted_G1;$x++)
			{ print OUT "\t\t\{\n\t\tname: \"$sorted_G1[$x][2]\",\n\t\treads: \"$sorted_G1[$x][1]\",\n\t\tpercentage\: \"$sorted_G1[$x][0]\",\n\t\tnotes\:\"sample possibly mixed-mycobacterial; refer to Mykrobe report\"\n\t\t\},\n"; }
		  print OUT "\t]\n";
		}
	}
print OUT "\}\n";
close(OUT) or die $!;
exit 1;