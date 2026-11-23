import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Layout } from './components/common/Layout';
import { LandingPage } from './pages/LandingPage';
import { DashboardPage } from './pages/DashboardPage';
import { TranslatorPage } from './pages/TranslatorPage';
import { LiveLecturePage } from './pages/LiveLecturePage';
import { DocumentTranslatorPage } from './pages/DocumentTranslatorPage';
import { VocabularyExplorerPage } from './pages/VocabularyExplorerPage';
import { ValidationPortalPage } from './pages/ValidationPortalPage';
import { HistoryPage } from './pages/HistoryPage';
import { AvatarSettingsPage } from './pages/AvatarSettingsPage';
import { AvatarAuditComparisonPage } from './pages/AvatarAuditComparisonPage';
import { ExpertReviewPortalPage } from './pages/ExpertReviewPortalPage';
import { CommunityEvaluationPage } from './pages/CommunityEvaluationPage';
import { ValidationDashboardPage } from './pages/ValidationDashboardPage';
import { OutreachDashboardPage } from './pages/OutreachDashboardPage';
import { LiveDemoPage } from './pages/LiveDemoPage';
import { AboutPage } from './pages/AboutPage';

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<LandingPage />} />
          <Route path="demo" element={<LiveDemoPage />} />
          <Route path="dashboard" element={<DashboardPage />} />
          <Route path="translate" element={<TranslatorPage />} />
          <Route path="live-lecture" element={<LiveLecturePage />} />
          <Route path="documents" element={<DocumentTranslatorPage />} />
          <Route path="vocabulary" element={<VocabularyExplorerPage />} />
          <Route path="validation" element={<ValidationPortalPage />} />
          <Route path="expert-review" element={<ExpertReviewPortalPage />} />
          <Route path="community-evaluation" element={<CommunityEvaluationPage />} />
          <Route path="validation-dashboard" element={<ValidationDashboardPage />} />
          <Route path="outreach" element={<OutreachDashboardPage />} />
          <Route path="history" element={<HistoryPage />} />
          <Route path="avatar-settings" element={<AvatarSettingsPage />} />
          <Route path="avatar-audit" element={<AvatarAuditComparisonPage />} />
          <Route path="about" element={<AboutPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};

export default App;

