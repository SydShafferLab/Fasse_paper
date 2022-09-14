# Fasse_paper
AJF009 ANALYSIS SCRIPTS

Folder of outs: /Volumes/GoogleDrive/My Drive/Fasse_Shared/AJF_Drive_copy/
Experiments/AJF009/2022_01_14_analysis_scripts/2022_05_27_analysis

Folder of scripts: /Users/ariafasse/Documents/GitHub/Fasse_paper

THIS IS THE CORRECT ORDER TO RUN SCRIPTS

## EXAMPLE: Folder name (type of data)
#### Input: 
```
```
#### Function:
```
```
#### Output: 
```
R object names (file_name)
```

## preprocess_gDNA (gDNA only)
#### Input: 
```
starcode outputs
FeatureReference_filtered.csv
```
#### Function: 
```
Adds lineage names
Concatenates fastqs from each sample
Performs RPM normalization
Generates basic statistic plots
```
#### Output:
```
gDNA_basic_stats, gDNA_files, gDNA_collapsed (preprocessed_gDNA.RData)
gDNA_anno (full_preprocessed_gDNA.RData)
Barcode rank order plots
```

## filtering_gDNA (gDNA only)
#### Input: 
```
preprocessed_gDNA
```
#### Function:
```
Identifies spike-ins
Tries different filtering options
Filters based on lineages with reads of at least 50 cells in shared 1st condition group
Finds filtering statistics
```
#### Output: 
```
spikes, fifty_cell_spikes (spikes.RData)
filtered_lins_list, filtered_matrix, firstcondition50 (filtered_gDNA.RData)
gDNA_filtered_stats.csv
Spike-in regression plots
Filtering venn plots
```

## Lineage_heatmaps (gDNA only)
#### Input: 
```
preprocessed_gDNA
filtered_gDNA
```
#### Function:
```
makes heatmaps of filtered_matrix ordered by lineage size
```
#### Output: 
```
Heatmaps for full, top 1000, top 50 lineages per condition
```

## Preprocess_GEX (cDNA only)
#### Input: 
```
filtered_feature_bc_matrix for each sample
```
#### Function:
```
filters, normalizes, runs PCA and UMAP
```
#### Output: 
```
Plots of individual condition clusters and markers
Individual objects (objects_premerged.RData)
All_data (object_postmerge.RData)
All_data with condition names (all_data_merged.RData)
First_timepoint, second_timepoint, dabtram_both_times (timepoint_separated_postmerge.RData)
EACH OBJECT WITH CONDITION NAMES (object_name.RData)
```

## Test_barcode_assignment
#### Input: 
```
all_data_merged.RData
FeatureReference_filtered.csv
```
#### Function:
```
Finds number unique barcodes per cell and cells per barcode
Finds read cutoffs for max # single and max difference between single and multiple barcodes
Assign dominant barcodes if highly expressed
Determined that collapse_single keeps highest number of single barcode cells
```
#### Output: 
```
lineage_count_cutoffs.RData
Table_fam_max_single.csv
Table_fam_max_difference.csv
Table_collapse_single.csv
Table_collapse_difference.csv
```

## Assign_dominant_barcodes
#### Input: 
```
all_data_merged.RData
objects_premerged.RData
dabtram_both_times.RData
FeatureReference_filtered.csv
lineage_count_cutoffs.RData
```
#### Function:
```
Filters cells based on max_single determined in test barcode assignment
Writes final barcode assignments to Seurat metadata
```
#### Output: 
```
All_data (all_data_final_lineages.RData)
dabtram_both_times_final_lineages.RData
dabtram_final_lineages.RData
cocl2_final_lineages.RData
cis_final_lineages.RData
```

## Lineages_per_condition
#### Input: 
```
all_data_final_lineages.RData
```
#### Function:
```
Finds # cells and unique lineages per condition
```
#### Output: 
```
Lineages_and_cells_per.csv
```

## Filtering_cDNA (cDNA only)
#### Input: 
```
all_data_final_lineages.RData
preprocessed_gDNA.RData
filtered_gDNA.RData
```
#### Function:
```
Plot cDNA cells versus gDNA reads per lineage per condition
Combine unfiltered cDNA and gDNA
Venn plot how many lineages overlap or are lost in filtering each dataset
Check size of cDNA lineages that are filtered out from gDNA filtering alone
Add back in any cDNA lineages of 50+ cells to resistant lin list
Combine cDNA and gDNA resistant lineage lists
Find induced resistant lineages
Find lineages resistant to many conditions (overlapping)
```
#### Output: 
```
Resistant_lineage_RPM_cutoffs.csv
cDNA_versus_gDNA_lineages.pdf
cDNA_lineage_size_filtering.pdf
gDNA_cDNA_collapsed, filtered_lins_list_cDNA, firstcondition50_cDNA (filtered_cDNA.RData)
combined_lins_list, induced_resistant_lins, overlapping_lins, fivecell_cDNA (resistant_lineage_lists.RData)
```

## Condition_clustering
#### Input: 
```
Objects_premerged.RData
second_timepoint_merged.RData
first_timepoint_merged.RData
```
#### Function:
```
Does everything on both second_timepoint and all_data objects but only second_timepoint is used in figures
Clusters all_data with varying cluster numbers
Finds drug condition of cells in each cluster
Repeats this looking at shared 1st and 2nd drug groups
Highlights cells in UMAP space with shared 1st and 2nd drug groups
```
#### Output: 
```
all_data_13cluster.RData
all_data_7cluster.RData
Original_condition_second_timepoint.pdf
original_condition_second_timepoint_cluster', i-1, '.pdf
end_condition_second_timepoint', i-1, '.pdf
first_condition_second_timepoint', i-1, '.pdf
drug_group_highlights.pdf
```

## Lineage_expression
#### Input: 
```
all_data_final_lineages.RData
second_timepoint_merged.RData
resistant_lineage_lists.RData
cis_final_lineages.RData
cocl2_final_lineages.RData
dabtram_final_lineages.RData
dabtram_both_times_final_lineages.RData
```
#### Function:
```
Plots cell cycle
Finds markers within each first drug object to look for subgroups
Builds filtered_meta Idents to say if each cell is in resistant, large resistant, or filtered lineages 
Plots expression of egfr/ngfr per lineage >5 cells over time in dabtram as violin
Highlights cells in UMAP space in switching vs stable lineages
Finds egfr/ngfr score per lineage over time in dabtram, plots as heatmap
	Identifies how these lineages grow in other drugs after dabtram as well
Assesses whether cells from the same lineage are more likely to be in the same cluster than by random changce for each drug condition
	Plots the test statistics
Identifies which clusters have lineages with only a single cell in them (singlets)
```
#### Output: 
```
all_data_markers.RData
Clusters_per_lin_dabtram.pdf
Clusters_per_lin_dabtramtodabtram.pdf
test_violin.pdf
stacked_bar_EGFR_NGFR_Died.pdf
stacked_bar_EGFR_NGFR_Died_w_other_second_drugs.pdf
<drug_condition>_sim_results.RData
sim_results.csv
proportion_clusters_heatmaps_rowclust.pdf
proportion_clusters_heatmaps.pdf
weighted_mean_cluster_assignments_test_stats_diffyaxes.pdf
weighted_mean_cluster_assignments_test_stats.pdf
singlets.xlsx
singlets_on_umap.pdf
```

## Induced_resistance
#### Input: 
```
```
#### Function:
```
```
#### Output: 
```

```

## Scripts not used in this iteration of analysis (not on github):
Find_induced_resistant_markers
Loads in all_data_final_lineages, x_final_lineages, x_first_final_lineages,  induced_resistant_lineage_lists
	Looks for markers of induced resistant vs all other lineages after 1st drug
Exports x_inducedto_x_markers.pdf 


Induced_resistant_markers_from_endstate
Loads in all_data_final_lineages, x_final_lineages, x_first_final_lineages,  induced_resistant_lineage_lists
Looks for expression of endstate markers in induced resistant vs all other lineages after 1st drug
Exports cluster_markers.RData, x_inducedto_x_markers_endstate.pdf
