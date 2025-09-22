export interface OCRResult {
  extracted_text: string;
  confidence?: number;
  processing_method?: string;
}

export interface FrequencyResult {
  frequency_vector: Array<{glyph: string, frequency: number}>;
  harmonic_analysis?: {
    harmonic_mean: number;
    adjusted_mean: number;
    cultural_modifier: number;
    spiritual_context: string;
  };
  brett_method_validation?: boolean;
}

export interface NarrativeResult {
  narrative: string;
  cultural_context?: string;
  glyph_count?: number;
  methodology?: string;
  confidence_level?: number;
}

export interface ValidationResult {
  valid: boolean;
  arithmetic_mean?: number;
  harmonic_mean?: number;
  frequency_category?: string;
  pattern_consistency?: number;
  brett_method_compliant?: boolean;
  validation_details?: {
    range_valid: boolean;
    pattern_valid: boolean;
    consistency_valid: boolean;
  };
}
