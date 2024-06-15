---
layout: post
title: GATK pipeline, at a glance
categories: [blog]
tags: [gatk, bioinformatics]
---

Examples to serve as a guide for analyses using [GATK](https://software.broadinstitute.org/gatk/). Version used is 3.2.2. It is best to consult the tool documentation for in-depth discussion of the parameters and outputs.

Set paths to tools
```bash
bwa="/opt/bwa/gcc-4.8.2_bwa-0.7.10/bwa"
picardtools="java -jar -Xmx10g -XX:ParallelGCThreads=1 /home/mroa/bin/picard-tools-1.119"
samtools="/home/mroa/bin/samtools-1.0/samtools"
gatk="java -jar /home/mroa/bin/GenomeAnalysisTK-3.2-2/GenomeAnalysisTK.jar"
```
<!--more-->

More paths to directories, inputs and outputs
```bash
WORKDIR=/home/mroa/data
LANE=lane3  ## when working with multiple samples from the same lane
REFDIR=$WORKDIR/reference
REFERENCE=$REFDIR/reference.fasta
REFINDEX=$REFERENCE
REFDICT=$REFDIR/reference.dict
OUTDIR=$WORKDIR/snps/$LANE
DATADIR=$WORKDIR/demultiplex/$LANE
SNPSDIR=$WORKDIR/snps
```

Do this once for each reference
```bash
bwa index $REFERENCE &&
$picardtools/CreateSequenceDictionary.jar REFERENCE=$REFERENCE OUTPUT=$REFDICT &&
$samtools faidx $REFERENCE &&
```

Do this for all FASTQ pairs
```bash
for num in {1..96}; do
    READ=sample$num
    LOGTIME=$WORKDIR/snps/$LANE/timelogs/$READ
    mkdir -p $LOGTIME
    READ1=$DATADIR/$READ\_1.fastq
    READ2=$DATADIR/$READ\_2.fastq
    SNPSDIR=$WORKDIR/snps

    bwa mem -t 20 $REFINDEX $READ1 $READ2 > $READ.sam &&
    $picardtools/SortSam.jar SO=coordinate INPUT=$READ.sam OUTPUT=$READ.sorted.bam VALIDATION_STRINGENCY=LENIENT CREATE_INDEX=TRUE &&
    $picardtools/FixMateInformation.jar SO=coordinate INPUT=$READ.sorted.bam OUTPUT=$READ.fixmate.bam VALIDATION_STRINGENCY=LENIENT CREATE_INDEX=TRUE &&
    $picardtools/MarkDuplicates.jar INPUT=$READ.fixmate.bam OUTPUT=$READ.markdup.bam METRICS_FILE=$READ.metrics VALIDATION_STRINGENCY=LENIENT CREATE_INDEX=TRUE MAX_FILE_HANDLES_FOR_READ_ENDS_MAP=1000 &&
    $picardtools/AddOrReplaceReadGroups.jar INPUT=$READ.markdup.bam OUTPUT=$READ.adrg.bam RGID=$READ LB=$READ PL='Illumina' SM=$READ CN="" RGPU=$READ VALIDATION_STRINGENCY=LENIENT SO=coordinate CREATE_INDEX=TRUE &&
    $gatk -T RealignerTargetCreator -nt 20 -R $REFERENCE -I $READ.adrg.bam -o $READ.intervals &&
    $gatk -T IndelRealigner -I $READ.adrg.bam -R $REFERENCE -targetIntervals $READ.intervals -o $READ.realigned.bam

done
```

Do this once to merge all alignments
```bash
$samtools merge $SNPSDIR/Seq.merged.bam $SNPSDIR/lane1/*realigned.bam $SNPSDIR/lane2/*realigned.bam $SNPSDIR/lane3/*realigned.bam $SNPSDIR/lane4/*realigned.bam
$samtools index $SNPSDIR/Seq.merged.bam
```
Call SNPs
```bash
$gatk -T UnifiedGenotyper -nt 20 -R $REFERENCE -I $SNPSDIR/Seq.merged.bam -o $SNPSDIR/Seq.vcf.gz -glm SNP -mbq 20 --genotyping_mode DISCOVERY -out_mode EMIT_VARIANTS_ONLY
```
