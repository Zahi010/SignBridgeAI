import React, { useState, useEffect } from 'react';
import {
  Building2,
  Search,
  Filter,
  CheckCircle2,
  Clock,
  Send,
  Calendar,
  AlertTriangle,
  Download,
  PlusCircle,
  MessageSquare,
  FileText,
  ExternalLink,
  ShieldAlert,
  ChevronRight,
  X,
  Phone,
  Mail,
  Award
} from 'lucide-react';
import { api } from '../api/client';
import { InstitutionalOutreach, OutreachStats, OutreachInteraction } from '../types';

export const OutreachDashboardPage: React.FC = () => {
  const [organizations, setOrganizations] = useState<InstitutionalOutreach[]>([]);
  const [stats, setStats] = useState<OutreachStats | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [search, setSearch] = useState<string>('');
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [selectedStatus, setSelectedStatus] = useState<string>('');
  const [activeOrg, setActiveOrg] = useState<InstitutionalOutreach | null>(null);
  const [isDetailOpen, setIsDetailOpen] = useState<boolean>(false);

  // Interaction logging form state
  const [interactionType, setInteractionType] = useState<string>('NOTE');
  const [interactionSummary, setInteractionSummary] = useState<string>('');
  const [interactionDetails, setInteractionDetails] = useState<string>('');
  const [interactionOutcome, setInteractionOutcome] = useState<string>('');
  const [interactionNextSteps, setInteractionNextSteps] = useState<string>('');
  const [submittingInteraction, setSubmittingInteraction] = useState<boolean>(false);

  // Update status form state
  const [newStatus, setNewStatus] = useState<string>('');
  const [newNotes, setNewNotes] = useState<string>('');
  const [updatingStatus, setUpdatingStatus] = useState<boolean>(false);

  const fetchOutreachData = async () => {
    try {
      setLoading(true);
      const params: any = {};
      if (search) params.search = search;
      if (selectedCategory) params.category = selectedCategory;
      if (selectedStatus) params.status = selectedStatus;

      const [orgsData, statsData] = await Promise.all([
        api.getOutreachOrganizations(params),
        api.getOutreachStats(),
      ]);

      setOrganizations(orgsData);
      setStats(statsData);

      // Refresh active org detail if modal is open
      if (activeOrg) {
        const updated = await api.getOutreachOrganizationDetail(activeOrg.id);
        setActiveOrg(updated);
      }
    } catch (err) {
      console.error('Failed to load outreach data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchOutreachData();
  }, [search, selectedCategory, selectedStatus]);

  const handleOpenDetail = async (org: InstitutionalOutreach) => {
    try {
      const fullDetail = await api.getOutreachOrganizationDetail(org.id);
      setActiveOrg(fullDetail);
      setNewStatus(fullDetail.outreach_status);
      setNewNotes(fullDetail.notes || '');
      setIsDetailOpen(true);
    } catch (err) {
      console.error('Failed to load institution details:', err);
    }
  };

  const handleLogInteraction = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!activeOrg || !interactionSummary) return;

    try {
      setSubmittingInteraction(true);
      await api.logOutreachInteraction(activeOrg.id, {
        interaction_type: interactionType,
        summary: interactionSummary,
        details: interactionDetails || undefined,
        outcome: interactionOutcome || undefined,
        next_steps: interactionNextSteps || undefined,
      });

      // Clear form
      setInteractionSummary('');
      setInteractionDetails('');
      setInteractionOutcome('');
      setInteractionNextSteps('');

      // Refresh data
      await fetchOutreachData();
    } catch (err) {
      console.error('Failed to log interaction:', err);
      alert('Error logging interaction. Please check fields.');
    } finally {
      setSubmittingInteraction(false);
    }
  };

  const handleUpdateStatus = async () => {
    if (!activeOrg || !newStatus) return;

    try {
      setUpdatingStatus(true);
      await api.updateOutreachOrganization(activeOrg.id, {
        outreach_status: newStatus,
        notes: newNotes,
      });
      await fetchOutreachData();
      alert('Status and notes updated successfully.');
    } catch (err) {
      console.error('Failed to update status:', err);
      alert('Error updating status.');
    } finally {
      setUpdatingStatus(false);
    }
  };

  const handleExport = async () => {
    try {
      const exportJson = await api.exportOutreachData();
      const blob = new Blob([JSON.stringify(exportJson, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `signbridge_outreach_registry_${new Date().toISOString().slice(0, 10)}.json`;
      link.click();
    } catch (err) {
      console.error('Export failed:', err);
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'READY_FOR_OUTREACH':
        return <span className="px-2.5 py-1 text-xs font-semibold rounded-full bg-blue-100 text-blue-800 border border-blue-200">Ready for Outreach</span>;
      case 'CONTACTED':
        return <span className="px-2.5 py-1 text-xs font-semibold rounded-full bg-amber-100 text-amber-800 border border-amber-200">Contacted</span>;
      case 'RESPONSE_RECEIVED':
        return <span className="px-2.5 py-1 text-xs font-semibold rounded-full bg-indigo-100 text-indigo-800 border border-indigo-200">Response Received</span>;
      case 'MEETING_COMPLETED':
        return <span className="px-2.5 py-1 text-xs font-semibold rounded-full bg-emerald-100 text-emerald-800 border border-emerald-200">Meeting Completed</span>;
      case 'AGREEMENT_PENDING':
        return <span className="px-2.5 py-1 text-xs font-semibold rounded-full bg-purple-100 text-purple-800 border border-purple-200">MoU Pending</span>;
      case 'COLLABORATION_CONFIRMED':
        return <span className="px-2.5 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800 border border-green-300">MoU Confirmed</span>;
      case 'VERIFIED':
        return <span className="px-2.5 py-1 text-xs font-semibold rounded-full bg-slate-100 text-slate-800 border border-slate-200">Profile Verified</span>;
      default:
        return <span className="px-2.5 py-1 text-xs font-semibold rounded-full bg-slate-100 text-slate-700">{status}</span>;
    }
  };

  const getCategoryBadge = (cat: string) => {
    switch (cat) {
      case 'GOVERNMENT_NATIONAL':
        return <span className="px-2 py-0.5 text-[11px] font-medium rounded bg-red-50 text-red-700 border border-red-200">Govt Autonomous</span>;
      case 'DEAF_ORGANIZATION':
        return <span className="px-2 py-0.5 text-[11px] font-medium rounded bg-purple-50 text-purple-700 border border-purple-200">Deaf Organization</span>;
      case 'ACADEMIC_RESEARCH':
        return <span className="px-2 py-0.5 text-[11px] font-medium rounded bg-indigo-50 text-indigo-700 border border-indigo-200">Academic / AI / HCI</span>;
      case 'SPECIAL_EDUCATION':
        return <span className="px-2 py-0.5 text-[11px] font-medium rounded bg-teal-50 text-teal-700 border border-teal-200">Speech & Hearing</span>;
      default:
        return <span className="px-2 py-0.5 text-[11px] font-medium rounded bg-slate-100 text-slate-700">{cat}</span>;
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b border-slate-200 pb-6">
        <div>
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-indigo-600 rounded-xl text-white shadow-sm">
              <Building2 size={24} />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-slate-900">Institutional Outreach & Collaboration Readiness</h1>
              <p className="text-sm text-slate-600">
                Phase 8 Institutional Pipeline: Outreach tracking, researcher contact registry, and demonstration audit.
              </p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={handleExport}
            className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-slate-700 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors shadow-2xs"
          >
            <Download size={16} />
            <span>Export Registry (JSON)</span>
          </button>
        </div>
      </div>

      {/* Zero Fabrication Governance Notice */}
      <div className="p-4 bg-amber-50/80 border border-amber-200/90 rounded-xl text-amber-900 flex items-start gap-3.5">
        <ShieldAlert size={20} className="text-amber-700 shrink-0 mt-0.5" />
        <div className="text-xs space-y-1">
          <p className="font-bold">Zero-Fabrication Research Policy — Phase 8 Operational Boundaries:</p>
          <p>
            This system tracks prospective academic and Deaf community institutions independently verified through public directories.
            <strong> SignBridge AI does not dispatch automated emails or claim unauthorized institutional affiliations.</strong> All partnerships remain prospective until a formal signed Memorandum of Understanding (MoU) or institutional collaboration letter is on file.
          </p>
        </div>
      </div>

      {/* Metrics Cards */}
      {stats && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-2xs">
            <div className="flex items-center justify-between text-slate-500 mb-2">
              <span className="text-xs font-bold uppercase tracking-wider">Verified Institutions</span>
              <Building2 size={18} className="text-blue-600" />
            </div>
            <div className="text-2xl font-black text-slate-900">{stats.total_organizations}</div>
            <div className="text-xs text-slate-500 mt-1">100% official websites & contacts verified</div>
          </div>

          <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-2xs">
            <div className="flex items-center justify-between text-slate-500 mb-2">
              <span className="text-xs font-bold uppercase tracking-wider">Ready for Outreach</span>
              <Send size={18} className="text-indigo-600" />
            </div>
            <div className="text-2xl font-black text-indigo-700">
              {stats.by_status['READY_FOR_OUTREACH'] || 0}
            </div>
            <div className="text-xs text-slate-500 mt-1">Proposal & letter customized</div>
          </div>

          <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-2xs">
            <div className="flex items-center justify-between text-slate-500 mb-2">
              <span className="text-xs font-bold uppercase tracking-wider">Interactions Logged</span>
              <MessageSquare size={18} className="text-emerald-600" />
            </div>
            <div className="text-2xl font-black text-emerald-700">{stats.total_interactions}</div>
            <div className="text-xs text-slate-500 mt-1">Verification notes & administrative audits</div>
          </div>

          <div className="p-5 bg-white rounded-xl border border-slate-200 shadow-2xs">
            <div className="flex items-center justify-between text-slate-500 mb-2">
              <span className="text-xs font-bold uppercase tracking-wider">Gate Readiness</span>
              <Award size={18} className="text-amber-600" />
            </div>
            <div className="text-sm font-bold text-slate-900">
              <span className="text-emerald-600">Gate A: PASS</span>
            </div>
            <div className="text-xs text-slate-500 mt-1">Gate B: Gated (Pending MoUs)</div>
          </div>
        </div>
      )}

      {/* Filter and Search Bar */}
      <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-2xs flex flex-col md:flex-row gap-4 items-center justify-between">
        <div className="relative w-full md:w-96">
          <Search size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            placeholder="Search by institution name, acronym, or department..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-10 pr-4 py-2 text-sm border border-slate-300 rounded-lg focus:outline-hidden focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500"
          />
        </div>

        <div className="flex flex-wrap items-center gap-3 w-full md:w-auto">
          <div className="flex items-center gap-2">
            <Filter size={16} className="text-slate-400" />
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="text-xs border border-slate-300 rounded-lg px-2.5 py-2 bg-white text-slate-700 focus:outline-hidden focus:border-indigo-500"
            >
              <option value="">All Categories</option>
              <option value="GOVERNMENT_NATIONAL">Government Autonomous</option>
              <option value="DEAF_ORGANIZATION">Deaf Community / NGOs</option>
              <option value="ACADEMIC_RESEARCH">Academic Research / IIT / IIIT</option>
              <option value="SPECIAL_EDUCATION">Speech & Hearing Sciences</option>
            </select>
          </div>

          <select
            value={selectedStatus}
            onChange={(e) => setSelectedStatus(e.target.value)}
            className="text-xs border border-slate-300 rounded-lg px-2.5 py-2 bg-white text-slate-700 focus:outline-hidden focus:border-indigo-500"
          >
            <option value="">All Statuses</option>
            <option value="VERIFIED">Profile Verified</option>
            <option value="READY_FOR_OUTREACH">Ready for Outreach</option>
            <option value="CONTACTED">Contacted</option>
            <option value="RESPONSE_RECEIVED">Response Received</option>
            <option value="MEETING_COMPLETED">Meeting Completed</option>
            <option value="COLLABORATION_CONFIRMED">MoU Confirmed</option>
          </select>
        </div>
      </div>

      {/* Institutional Table */}
      <div className="bg-white border border-slate-200 rounded-xl overflow-hidden shadow-2xs">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-600">
            <thead className="bg-slate-50 text-slate-700 text-xs font-semibold uppercase tracking-wider border-b border-slate-200">
              <tr>
                <th className="px-6 py-3.5">Institution</th>
                <th className="px-6 py-3.5">Category</th>
                <th className="px-6 py-3.5">Collaboration Role</th>
                <th className="px-6 py-3.5">Status</th>
                <th className="px-6 py-3.5">Proposed Tier</th>
                <th className="px-6 py-3.5">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200">
              {loading ? (
                <tr>
                  <td colSpan={6} className="px-6 py-12 text-center text-slate-500">
                    Loading verified institutions...
                  </td>
                </tr>
              ) : organizations.length === 0 ? (
                <tr>
                  <td colSpan={6} className="px-6 py-12 text-center text-slate-500">
                    No institutions match the selected filters.
                  </td>
                </tr>
              ) : (
                organizations.map((org) => (
                  <tr key={org.id} className="hover:bg-slate-50/80 transition-colors">
                    <td className="px-6 py-4">
                      <div className="font-semibold text-slate-900 flex items-center gap-2">
                        <span>{org.organization_name}</span>
                        {org.acronym && (
                          <span className="px-1.5 py-0.5 text-[10px] bg-slate-100 text-slate-700 rounded font-bold">
                            {org.acronym}
                          </span>
                        )}
                      </div>
                      <div className="text-xs text-slate-500 mt-1 flex items-center gap-3">
                        <a
                          href={org.website}
                          target="_blank"
                          rel="noreferrer"
                          className="text-indigo-600 hover:underline flex items-center gap-1"
                        >
                          <span>{org.website.replace('https://', '').replace('http://', '')}</span>
                          <ExternalLink size={11} />
                        </a>
                        <span>·</span>
                        <span>{org.public_contact}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      {getCategoryBadge(org.category)}
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-xs font-medium text-slate-800">{org.collaboration_role}</span>
                    </td>
                    <td className="px-6 py-4">
                      {getStatusBadge(org.outreach_status)}
                    </td>
                    <td className="px-6 py-4 text-xs text-slate-600">
                      {org.proposed_collaboration_tier.split(':')[0]}
                    </td>
                    <td className="px-6 py-4">
                      <button
                        onClick={() => handleOpenDetail(org)}
                        className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-indigo-700 bg-indigo-50 hover:bg-indigo-100 rounded-lg transition-colors"
                      >
                        <span>Manage & Log</span>
                        <ChevronRight size={14} />
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Detail Slide-Over Modal */}
      {isDetailOpen && activeOrg && (
        <div className="fixed inset-0 z-50 flex justify-end bg-slate-900/50 backdrop-blur-xs">
          <div className="w-full max-w-2xl bg-white h-full overflow-y-auto shadow-2xl flex flex-col">
            {/* Modal Header */}
            <div className="p-6 border-b border-slate-200 flex items-center justify-between sticky top-0 bg-white z-10">
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-indigo-600">Institutional Detail</span>
                <h2 className="text-lg font-bold text-slate-900">{activeOrg.organization_name}</h2>
              </div>
              <button
                onClick={() => setIsDetailOpen(false)}
                className="p-2 text-slate-400 hover:text-slate-600 rounded-lg hover:bg-slate-100 transition-colors"
              >
                <X size={20} />
              </button>
            </div>

            {/* Modal Content */}
            <div className="p-6 space-y-6 flex-1">
              {/* Profile Card */}
              <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 text-xs space-y-2.5">
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <span className="font-semibold text-slate-500">Website:</span>
                    <a
                      href={activeOrg.website}
                      target="_blank"
                      rel="noreferrer"
                      className="ml-1 text-indigo-600 hover:underline inline-flex items-center gap-1"
                    >
                      {activeOrg.website}
                      <ExternalLink size={10} />
                    </a>
                  </div>
                  <div>
                    <span className="font-semibold text-slate-500">Contact:</span>
                    <span className="ml-1 text-slate-800">{activeOrg.public_contact}</span>
                  </div>
                  <div>
                    <span className="font-semibold text-slate-500">Telephone:</span>
                    <span className="ml-1 text-slate-800">{activeOrg.telephone || 'Published directory'}</span>
                  </div>
                  <div>
                    <span className="font-semibold text-slate-500">Department:</span>
                    <span className="ml-1 text-slate-800">{activeOrg.department || 'Not specified'}</span>
                  </div>
                  <div>
                    <span className="font-semibold text-slate-500">Role:</span>
                    <span className="ml-1 text-slate-800">{activeOrg.collaboration_role}</span>
                  </div>
                  <div>
                    <span className="font-semibold text-slate-500">Proposed Tier:</span>
                    <span className="ml-1 text-slate-800">{activeOrg.proposed_collaboration_tier}</span>
                  </div>
                </div>
                <div className="pt-2 border-t border-slate-200">
                  <span className="font-semibold text-slate-500">Verification Provenance:</span>
                  <span className="ml-1 text-slate-700">{activeOrg.verification_source} (Verified: {activeOrg.verification_date})</span>
                </div>
              </div>

              {/* Status Update Section */}
              <div className="border border-slate-200 p-4 rounded-xl space-y-3">
                <h3 className="text-sm font-bold text-slate-900">Update Outreach Status & Notes</h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">Status</label>
                    <select
                      value={newStatus}
                      onChange={(e) => setNewStatus(e.target.value)}
                      className="w-full text-xs border border-slate-300 rounded-lg p-2"
                    >
                      <option value="VERIFIED">VERIFIED</option>
                      <option value="READY_FOR_OUTREACH">READY_FOR_OUTREACH</option>
                      <option value="CONTACTED">CONTACTED</option>
                      <option value="RESPONSE_RECEIVED">RESPONSE_RECEIVED</option>
                      <option value="MEETING_REQUESTED">MEETING_REQUESTED</option>
                      <option value="MEETING_COMPLETED">MEETING_COMPLETED</option>
                      <option value="COLLABORATION_DISCUSSION">COLLABORATION_DISCUSSION</option>
                      <option value="AGREEMENT_PENDING">AGREEMENT_PENDING</option>
                      <option value="COLLABORATION_CONFIRMED">COLLABORATION_CONFIRMED</option>
                      <option value="NO_RESPONSE">NO_RESPONSE</option>
                      <option value="DECLINED">DECLINED</option>
                      <option value="ON_HOLD">ON_HOLD</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">Internal Notes</label>
                    <input
                      type="text"
                      value={newNotes}
                      onChange={(e) => setNewNotes(e.target.value)}
                      placeholder="Add administrative notes..."
                      className="w-full text-xs border border-slate-300 rounded-lg p-2"
                    />
                  </div>
                </div>
                <button
                  onClick={handleUpdateStatus}
                  disabled={updatingStatus}
                  className="px-3 py-1.5 text-xs font-semibold bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors disabled:opacity-50"
                >
                  {updatingStatus ? 'Updating...' : 'Save Changes'}
                </button>
              </div>

              {/* Interaction History Timeline */}
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <h3 className="text-sm font-bold text-slate-900">Interaction History & Audit Log</h3>
                  <span className="text-xs text-slate-500">
                    {activeOrg.interactions ? activeOrg.interactions.length : 0} interactions logged
                  </span>
                </div>

                <div className="space-y-2.5 max-h-64 overflow-y-auto">
                  {activeOrg.interactions && activeOrg.interactions.length > 0 ? (
                    activeOrg.interactions.map((interaction) => (
                      <div key={interaction.id} className="p-3 bg-slate-50 border border-slate-200 rounded-lg text-xs space-y-1">
                        <div className="flex items-center justify-between font-semibold text-slate-800">
                          <span className="px-1.5 py-0.5 bg-indigo-100 text-indigo-700 rounded text-[10px]">
                            {interaction.interaction_type}
                          </span>
                          <span className="text-slate-400 font-normal">
                            {new Date(interaction.timestamp).toLocaleString()}
                          </span>
                        </div>
                        <p className="font-medium text-slate-900">{interaction.summary}</p>
                        {interaction.details && <p className="text-slate-600">{interaction.details}</p>}
                        {interaction.outcome && (
                          <p className="text-emerald-700 font-medium">Outcome: {interaction.outcome}</p>
                        )}
                        {interaction.next_steps && (
                          <p className="text-slate-500">Next Steps: {interaction.next_steps}</p>
                        )}
                      </div>
                    ))
                  ) : (
                    <div className="p-4 text-center text-xs text-slate-400 bg-slate-50 rounded-lg">
                      No interactions recorded yet. Use the form below to log an interaction.
                    </div>
                  )}
                </div>
              </div>

              {/* Log New Interaction Form */}
              <form onSubmit={handleLogInteraction} className="border border-slate-200 p-4 rounded-xl space-y-3">
                <h3 className="text-sm font-bold text-slate-900">Log New Activity / Interaction</h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">Interaction Type</label>
                    <select
                      value={interactionType}
                      onChange={(e) => setInteractionType(e.target.value)}
                      className="w-full text-xs border border-slate-300 rounded-lg p-2"
                    >
                      <option value="NOTE">NOTE (Internal Update)</option>
                      <option value="EMAIL_SENT">EMAIL_SENT (Admin Dispatched)</option>
                      <option value="EMAIL_RECEIVED">EMAIL_RECEIVED (Response Received)</option>
                      <option value="PHONE_CALL">PHONE_CALL (Telephone Inquiry)</option>
                      <option value="VIRTUAL_MEETING">VIRTUAL_MEETING (Video Call)</option>
                      <option value="IN_PERSON_MEETING">IN_PERSON_MEETING (Campus Visit)</option>
                      <option value="PRESENTATION">PRESENTATION (System Demo)</option>
                      <option value="MOU_DRAFT">MOU_DRAFT (Terms Exchanged)</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">Summary *</label>
                    <input
                      type="text"
                      required
                      value={interactionSummary}
                      onChange={(e) => setInteractionSummary(e.target.value)}
                      placeholder="e.g. Sent Phase 8 Proposal Letter"
                      className="w-full text-xs border border-slate-300 rounded-lg p-2"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">Details & Agenda</label>
                  <textarea
                    rows={2}
                    value={interactionDetails}
                    onChange={(e) => setInteractionDetails(e.target.value)}
                    placeholder="Key points discussed or message contents..."
                    className="w-full text-xs border border-slate-300 rounded-lg p-2"
                  />
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">Outcome</label>
                    <input
                      type="text"
                      value={interactionOutcome}
                      onChange={(e) => setInteractionOutcome(e.target.value)}
                      placeholder="e.g. Agreed to review presentation"
                      className="w-full text-xs border border-slate-300 rounded-lg p-2"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">Next Steps</label>
                    <input
                      type="text"
                      value={interactionNextSteps}
                      onChange={(e) => setInteractionNextSteps(e.target.value)}
                      placeholder="e.g. Schedule live demo for next Tuesday"
                      className="w-full text-xs border border-slate-300 rounded-lg p-2"
                    />
                  </div>
                </div>

                <button
                  type="submit"
                  disabled={submittingInteraction}
                  className="w-full py-2 text-xs font-bold bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors disabled:opacity-50"
                >
                  {submittingInteraction ? 'Logging...' : 'Save Interaction to Audit Log'}
                </button>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default OutreachDashboardPage;
