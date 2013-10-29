
def rna_cols( db ):
  eu = db.t_experiment_unit
  return [ eu.f_name ,
                       eu.f_sample ,
                       eu.f_treatment ,
                       eu.f_prep_preformed_by ,
                       eu.f_lib_prep_protocol ,
                       eu.f_barcode ,
                       eu.f_desired_multiplexing ,
                       eu.f_read_length ,
                       eu.f_read_type ,
                       eu.f_desired_minimum_reads ]

def dna_cols( db ):
  eu = db.t_experiment_unit
  return [ eu.f_name ,
                       eu.f_sample ,
                       eu.f_treatment ,
                       eu.f_prep_preformed_by ,
                       eu.f_lib_prep_protocol ,
                       eu.f_barcode ,
                       eu.f_desired_multiplexing ,
                       eu.f_read_length ,
                       eu.f_read_type ,
                       eu.f_desired_minimum_reads ]

def exome_cols( db ):
  eu = db.t_experiment_unit
  return  [ eu.f_name ,
                       eu.f_sample ,
                       eu.f_treatment ,
                       eu.f_prep_preformed_by ,
                       eu.f_lib_prep_protocol ,
                       eu.f_barcode ,
                       eu.f_whole_exome_custom_capture ,
                       eu.f_capture_protocol ,
                       eu.f_capture_size ,
                       eu.f_desired_multiplexing ,
                       eu.f_read_length ,
                       eu.f_read_type ,
                       eu.f_desired_minimum_reads ]

def chipseq_cols( db ):
  eu = db.t_experiment_unit
  return [ eu.f_name ,
                       eu.f_strain ,
                       eu.f_tissue ,
                       eu.f_source ,
                       eu.f_replicate ,
                       eu.f_agent ,
                       eu.f_target_symbol ,
                       eu.f_target_ID ,
                       eu.f_fb_wb_ID ,
                       eu.f_treatment ,
                       eu.f_prep_preformed_by ,
                       eu.f_lib_prep_protocol ,
                       eu.f_barcode ,
                       eu.f_desired_multiplexing ,
                       eu.f_read_length ,
                       eu.f_read_type ,
                       eu.f_desired_minimum_reads ]

def worm_cols( db ):
  return fly_cols( db )

def fly_cols( db ):
  eu = db.t_experiment_unit
  return [ eu.f_name , 
           eu.f_strain , 
           eu.f_tissue , 
           eu.f_stage , 
           eu.f_source , 
           eu.f_agent , 
           eu.f_replicate , 
           eu.f_flybase_wormbase_id , 
           eu.f_genotype , 
           eu.f_treatment , 
           eu.f_prep_preformed_by ,
           eu.f_lib_prep_protocol ,
           eu.f_barcode , 
           eu.f_desired_multiplexing ,
           eu.f_read_length , 
           eu.f_read_type , 
           eu.f_desired_minimum_reads , 
           eu.f_sample  ]
