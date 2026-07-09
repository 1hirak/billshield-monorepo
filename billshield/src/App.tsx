import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AppLayout } from "@/components/layout/AppLayout";
import { ErrorBoundary } from "@/components/ErrorBoundary";
import LandingPage from "@/pages/LandingPage";
import OnboardingPage from "@/pages/OnboardingPage";
import BillUploadPage from "@/pages/BillUploadPage";
import BillReviewPage from "@/pages/BillReviewPage";
import DashboardPage from "@/pages/DashboardPage";
import ScenarioSimulatorPage from "@/pages/ScenarioSimulatorPage";
import SupportMapPage from "@/pages/SupportMapPage";
import ThirtyDayPlanPage from "@/pages/ThirtyDayPlanPage";
import SettingsPage from "@/pages/SettingsPage";

export default function App() {
  return (
    <ErrorBoundary>
      <BrowserRouter>
        <Routes>
          <Route element={<AppLayout />}>
            <Route path="/" element={<LandingPage />} />
            <Route path="/onboarding" element={<OnboardingPage />} />
            <Route path="/upload" element={<BillUploadPage />} />
            <Route path="/review/:billId" element={<BillReviewPage />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/scenarios" element={<ScenarioSimulatorPage />} />
            <Route path="/support" element={<SupportMapPage />} />
            <Route path="/plan" element={<ThirtyDayPlanPage />} />
            <Route path="/settings" element={<SettingsPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </ErrorBoundary>
  );
}
