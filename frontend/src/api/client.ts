import axios from 'axios';
import {
  Branch,
  Subject,
  TranslationResponse,
  VocabularyListResponse,
  ConceptDetail,
  SignRecordDetail,
  TranslationHistoryItem,
  DocumentUploadResponse,
  PendingValidationItem,
  ReviewerValidationDecision
} from '../types';

const API_BASE = '/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

export const api = {
  // Health
  getHealth: async () => {
    const res = await apiClient.get('/health');
    return res.data;
  },

  // Branches & Subjects
  getBranches: async (): Promise<Branch[]> => {
    const res = await apiClient.get<Branch[]>('/branches');
    return res.data;
  },

  getSubjects: async (branchId?: number): Promise<Subject[]> => {
    const res = await apiClient.get<Subject[]>('/subjects', {
      params: branchId ? { branch_id: branchId } : {},
    });
    return res.data;
  },

  // Translation
  translate: async (payload: {
    text: string;
    branch_id?: number;
    subject_id?: number;
  }): Promise<TranslationResponse> => {
    const res = await apiClient.post<TranslationResponse>('/translate', payload);
    return res.data;
  },

  // Vocabulary
  getVocabulary: async (params?: {
    search?: string;
    branch_id?: number;
    validation_status?: string;
  }): Promise<VocabularyListResponse> => {
    const res = await apiClient.get<VocabularyListResponse>('/vocabulary', {
      params,
    });
    return res.data;
  },

  getConceptById: async (conceptId: number): Promise<ConceptDetail> => {
    const res = await apiClient.get<ConceptDetail>(`/vocabulary/${conceptId}`);
    return res.data;
  },

  getSignByConceptId: async (conceptId: number): Promise<SignRecordDetail> => {
    const res = await apiClient.get<SignRecordDetail>(`/signs/${conceptId}`);
    return res.data;
  },

  // Translation History
  getHistory: async (limit: number = 25): Promise<TranslationHistoryItem[]> => {
    const res = await apiClient.get<TranslationHistoryItem[]>('/history', {
      params: { limit },
    });
    return res.data;
  },

  // Document Upload
  uploadDocument: async (
    file: File,
    branchId?: number,
    subjectId?: number
  ): Promise<DocumentUploadResponse> => {
    const formData = new FormData();
    formData.append('file', file);
    if (branchId) formData.append('branch_id', branchId.toString());
    if (subjectId) formData.append('subject_id', subjectId.toString());

    const res = await apiClient.post<DocumentUploadResponse>(
      '/documents/upload',
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    return res.data;
  },

  // Expert Validation Workflow
  getReviewerProfiles: async (): Promise<import('../types').ReviewerProfile[]> => {
    const res = await apiClient.get<import('../types').ReviewerProfile[]>('/validation/reviewers');
    return res.data;
  },

  getPendingValidations: async (
    branchCode?: string,
    validationStatus: string = 'needs_review',
    limit: number = 50
  ): Promise<PendingValidationItem[]> => {
    const res = await apiClient.get<PendingValidationItem[]>('/validation/pending', {
      params: {
        branch_code: branchCode || undefined,
        validation_status: validationStatus,
        limit,
      },
    });
    return res.data;
  },

  getSignForValidation: async (signRecordId: number): Promise<SignRecordDetail> => {
    const res = await apiClient.get<SignRecordDetail>(`/validation/signs/${signRecordId}`);
    return res.data;
  },

  submitValidationDecision: async (payload: {
    sign_record_id: number;
    reviewer_profile_id?: number;
    reviewer_code?: string;
    reviewer_name: string;
    reviewer_role: string;
    affiliation?: string;
    decision: string;
    assigned_status: string;
    corrections?: string;
    suggested_regional_variation?: string;
    comments?: string;
    accuracy_rating?: number;
  }): Promise<{ id: number; message: string; assigned_status: string }> => {
    const res = await apiClient.post('/validation/submit', payload);
    return res.data;
  },

  getValidationAuditTrail: async (signRecordId: number): Promise<ReviewerValidationDecision[]> => {
    const res = await apiClient.get<ReviewerValidationDecision[]>(
      `/validation/audit-trail/${signRecordId}`
    );
    return res.data;
  },

  // Dataset Ingestion & Recording Session Endpoints
  getRecordingSessions: async (): Promise<import('../types').RecordingSession[]> => {
    const res = await apiClient.get<import('../types').RecordingSession[]>('/ingestion/recording-sessions');
    return res.data;
  },

  createRecordingSession: async (payload: {
    session_uid: string;
    signer_id: string;
    signer_name?: string;
    is_native_signer?: boolean;
    camera_setup?: string;
    lighting_environment?: string;
    background?: string;
    consent_status: string;
    consent_document_ref?: string;
    notes?: string;
  }): Promise<import('../types').RecordingSession> => {
    const res = await apiClient.post<import('../types').RecordingSession>('/ingestion/recording-session', payload);
    return res.data;
  },

  uploadSignVideo: async (formData: FormData): Promise<any> => {
    const res = await apiClient.post('/ingestion/sign-video', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return res.data;
  },

  uploadBatchDataset: async (file: File, format: 'json' | 'csv'): Promise<any> => {
    const formData = new FormData();
    formData.append('file', file);
    const res = await apiClient.post(`/ingestion/batch-${format}`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return res.data;
  },

  // Video & Avatar endpoints
  getVideoForConcept: async (conceptId: number) => {
    const res = await apiClient.get(`/videos/retrieve/${conceptId}`);
    return res.data;
  },

  getAvatarTimeline: async (irData: any) => {
    const res = await apiClient.post('/avatar/timeline', irData);
    return res.data;
  },

  // Speech-to-ISL endpoints
  transcribeAudio: async (audioFile: File | Blob, customHint?: string): Promise<any> => {
    const formData = new FormData();
    formData.append('file', audioFile, 'recording.wav');
    const params = customHint ? { custom_hint: customHint } : {};
    const res = await apiClient.post('/speech/transcribe', formData, {
      params,
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return res.data;
  },

  speechToISL: async (audioFile: File | Blob, branchId?: number, subjectId?: number): Promise<any> => {
    const formData = new FormData();
    formData.append('file', audioFile, 'recording.wav');
    if (branchId) formData.append('branch_id', String(branchId));
    if (subjectId) formData.append('subject_id', String(subjectId));
    const res = await apiClient.post('/speech/translate', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return res.data;
  },
};
