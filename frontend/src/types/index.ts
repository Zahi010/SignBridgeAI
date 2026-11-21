export type ValidationStatus = 
  | 'verified'
  | 'partial'
  | 'explanation_needed'
  | 'explanation_required'
  | 'needs_review'
  | 'unsupported'
  | 'demo_only'
  | 'blocked'
  | 'not_implemented';

export interface Branch {
  id: number;
  code: string;
  name: string;
  description?: string;
  subject_count: number;
  concept_count: number;
}

export interface Subject {
  id: number;
  branch_id: number;
  code: string;
  name: string;
  description?: string;
  concept_count: number;
}

export interface ExtractedConcept {
  id: number;
  term: string;
  category?: string;
  domain?: string;
  definition: string;
  difficulty_level: string;
  validation_status: ValidationStatus;
  disambiguation_rationale?: string;
  dominant_hand?: string | null;
  handshape?: string | null;
  movement?: string | null;
  location?: string | null;
  orientation?: string | null;
  non_manual_markers?: string | null;
  has_video: boolean;
  has_avatar: boolean;
  video_url?: string | null;
  source_attribution?: string | null;
  sign_gloss?: string | null;
  linguistic_notes?: string | null;
  reviewer_info?: string | null;
}

export interface GrammarNote {
  rule_type: string;
  english_pattern?: string;
  isl_structure: string;
  explanation: string;
  is_experimental_hypothesis?: boolean;
  validation_status?: string;
  disclaimer?: string;
}

export interface VideoOutput {
  available: boolean;
  title?: string;
  video_url?: string | null;
  thumbnail_url?: string | null;
  signer_name?: string | null;
  duration_seconds: number;
  resolution?: string;
  source_attribution?: string | null;
  license?: string | null;
  validation_status: ValidationStatus;
  notes?: string | null;
}

export interface AvatarOutput {
  available: boolean;
  model_type: string;
  animation_name?: string;
  rig_standard: string;
  validation_status: ValidationStatus;
  motion_status?: MotionVerificationStatus;
  notice: string;
}

export type MotionVerificationStatus = 
  | 'VERIFIED_ISL_MOTION'
  | 'PARTIALLY_VERIFIED_MOTION'
  | 'UNVERIFIED_MOTION'
  | 'DEMO_ONLY'
  | 'REQUIRES_LINGUISTIC_REVIEW'
  | 'NOT_IMPLEMENTED'
  | 'SOURCE_RESTRICTED';

export interface EulerAngles {
  x: number;
  y: number;
  z: number;
}

export interface FingerJointState {
  mcp: EulerAngles;
  pip: EulerAngles;
  dip: EulerAngles;
}

export interface HandPoseState {
  wrist: EulerAngles;
  thumb: FingerJointState;
  index: FingerJointState;
  middle: FingerJointState;
  ring: FingerJointState;
  pinky: FingerJointState;
}

export interface FacialBlendshapes {
  brow_furrow_left: number;
  brow_furrow_right: number;
  brow_raise_left: number;
  brow_raise_right: number;
  mouth_open: number;
  mouth_wide: number;
  eye_blink_left?: number;
  eye_blink_right?: number;
  head_pitch?: number;
  head_yaw?: number;
  head_roll?: number;
}

export interface AvatarKeyframe {
  timestamp_ms: number;
  chest_rotation?: EulerAngles;
  neck_rotation?: EulerAngles;
  head_rotation?: EulerAngles;
  left_shoulder_rotation?: EulerAngles;
  left_arm_rotation?: EulerAngles;
  left_forearm_rotation?: EulerAngles;
  left_hand?: HandPoseState;
  right_shoulder_rotation?: EulerAngles;
  right_arm_rotation?: EulerAngles;
  right_forearm_rotation?: EulerAngles;
  right_hand?: HandPoseState;
  facial_blendshapes?: FacialBlendshapes;
}

export interface AvatarAnimationTrack {
  track_id: string;
  track_type: string;
  gloss_token: string;
  concept_term?: string;
  start_time_seconds: number;
  duration_seconds: number;
  verification_status: MotionVerificationStatus;
  is_mocap: boolean;
  keyframes: AvatarKeyframe[];
  linguistic_disclaimer?: string;
}

export interface AvatarSequencePayload {
  sentence_text: string;
  overall_motion_status: MotionVerificationStatus;
  tracks: AvatarAnimationTrack[];
  total_duration_seconds: number;
  fps: number;
  rig_standard: string;
  policy_notice: string;
}

export interface AvatarStatusResponse {
  avatar_name: string;
  rig_standard: string;
  total_joints_count: number;
  finger_joints_count_per_hand: number;
  supported_facial_morph_targets: string[];
  motion_capture_pipeline_available: boolean;
  active_mocap_animations_count: number;
  status_breakdown: Record<string, number>;
  zero_fabrication_policy_enforced: boolean;
  disclaimer: string;
}

export interface PipelineStage {
  stage_id: string;
  stage_number: number;
  name: string;
  description: string;
  status: 'completed' | 'warning' | 'info' | 'error';
  duration_ms: number;
  summary: string;
  details: Record<string, any>;
}

export interface SemanticRelationship {
  source_concept: string;
  target_concept: string;
  relation_type: string;
  description: string;
}

export interface PedagogicalExplanation {
  term: string;
  category: string;
  why_unsupported: string;
  recommended_isl_strategy: string;
  fingerspelling_sequence?: string[];
  pedagogical_diagram_description?: string;
  engineering_definition?: string;
  technical_advice_for_educators?: string;
}

export interface TranslationResponse {
  id?: number;
  source_text: string;
  branch_name?: string | null;
  subject_name?: string | null;
  status: ValidationStatus;
  status_reason: string;
  extracted_concepts: ExtractedConcept[];
  semantic_relations?: SemanticRelationship[];
  pedagogical_explanations?: PedagogicalExplanation[];
  isl_gloss_sequence: string[];
  grammar_notes: GrammarNote[];
  intermediate_representation?: Record<string, any>;
  translation_plan?: Record<string, any>;
  video_output: VideoOutput;
  avatar_output: AvatarOutput;
  verified_signs_count: number;
  unsupported_signs_count: number;
  pipeline_stages?: PipelineStage[];
  total_pipeline_duration_ms?: number;
  unmatched_tokens?: string[];
  created_at: string;
}

export interface Provenance {
  id: number;
  name: string;
  organization: string;
  license: string;
  source_url?: string;
  methodology?: string;
  peer_reviewed: boolean;
}

export interface ExpertReview {
  id: number;
  reviewer_name: string;
  reviewer_role: string;
  affiliation?: string;
  status: ValidationStatus;
  review_notes?: string;
  sign_accuracy_rating?: number;
}

export interface ReviewerProfile {
  id: number;
  reviewer_code: string;
  full_name: string;
  is_certified_interpreter: boolean;
  is_deaf_native_signer: boolean;
  accreditation_body?: string;
  accreditation_number?: string;
  institution_affiliation?: string;
  qualifications?: string;
  is_authorized_expert: boolean;
  created_at: string;
}

export interface RecordingSession {
  id: number;
  session_uid: string;
  signer_id: string;
  signer_name?: string;
  is_native_signer: boolean;
  camera_setup: string;
  lighting_environment?: string;
  background?: string;
  consent_status: string;
  consent_document_ref?: string;
  created_at: string;
}

export interface ReviewerValidationDecision {
  id: number;
  sign_record_id: number;
  reviewer_name: string;
  reviewer_role: string;
  affiliation?: string;
  decision: string;
  assigned_status: ValidationStatus;
  corrections?: string;
  suggested_regional_variation?: string;
  comments?: string;
  accuracy_rating?: number;
  reviewed_at: string;
}

export interface SignVariant {
  id: number;
  variant_name: string;
  handshape?: string;
  movement?: string;
  location?: string;
  non_manual_features?: string;
}

export interface SignRecordDetail {
  id: number;
  sign_id?: string | null;
  sign_gloss: string;
  validation_status: ValidationStatus;
  is_authentic: boolean;
  linguistic_notes?: string;
  regional_dialect?: string;
  dominant_hand?: string | null;
  handshape?: string | null;
  movement?: string | null;
  location?: string | null;
  orientation?: string | null;
  non_manual_markers?: string | null;
  source_institution?: string | null;
  source_url_or_dataset_id?: string | null;
  license?: string | null;
  consent_info?: string | null;
  validation_date?: string | null;
  confidence_score?: number | null;
  provenance?: Provenance | null;
  expert_review?: ExpertReview | null;
  validation_reviews?: ReviewerValidationDecision[];
  variants: SignVariant[];
  has_video: boolean;
  video_url?: string | null;
}

export interface ConceptDetail {
  id: number;
  branch_id?: number | null;
  branch_name?: string | null;
  subject_id?: number | null;
  subject_name?: string | null;
  term: string;
  slug: string;
  aliases?: string;
  category?: string;
  domain?: string;
  definition: string;
  technical_context?: string;
  example_usage?: string;
  difficulty_level: string;
  validation_status: ValidationStatus;
  signs: SignRecordDetail[];
  created_at: string;
}

export interface VocabularyListResponse {
  total: number;
  verified_count: number;
  partial_count: number;
  unsupported_count: number;
  needs_review_count?: number;
  items: ConceptDetail[];
}

export interface PendingValidationItem {
  sign_record_id: number;
  sign_id?: string | null;
  concept_term: string;
  branch_name?: string | null;
  subject_name?: string | null;
  current_status: ValidationStatus;
  sign_gloss: string;
  regional_dialect?: string | null;
  has_video: boolean;
  has_animation: boolean;
  source_institution?: string | null;
  license?: string | null;
  review_count: number;
}

export interface TranslationHistoryItem {
  id: number;
  source_text: string;
  branch_name?: string | null;
  subject_name?: string | null;
  status: ValidationStatus;
  status_reason?: string | null;
  verified_signs_count: number;
  unsupported_signs_count: number;
  has_video: boolean;
  has_avatar: boolean;
  created_at: string;
}

export interface DocumentSection {
  section_index: number;
  heading: string;
  text_preview: string;
  sentence_count: number;
  detected_concepts: string[];
  supported_count: number;
  explanation_count: number;
  unsupported_count: number;
  status: string;
  isl_gloss_summary: string;
}

export interface DocumentAnalysis {
  total_sections: number;
  total_concepts_found: number;
  supported_concepts_count: number;
  explanation_required_count: number;
  unsupported_concepts_count: number;
  overall_status: string;
  coverage_percentage: number;
}

export interface DocumentUploadResponse {
  filename: string;
  file_type: string;
  file_size_bytes: number;
  page_or_slide_count: number;
  extracted_text_preview: string;
  total_words: number;
  total_sentences: number;
  detected_concepts_count: number;
  translation_summary: TranslationResponse;
  sections?: DocumentSection[];
  document_analysis?: DocumentAnalysis;
  uploaded_at: string;
}
