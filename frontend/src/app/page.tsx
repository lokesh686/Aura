"use client";

import { useState } from "react";

export default function Dashboard() {
  const [loading, setLoading] = useState(false);
  const [auditResult, setAuditResult] = useState<any>(null);

  // Custom Input State
  const [isCustomMode, setIsCustomMode] = useState(false);
  const [customResource, setCustomResource] = useState("user-data-bucket");
  const [customType, setCustomType] = useState("S3");
  const [customEncrypted, setCustomEncrypted] = useState(false);
  const [customPublic, setCustomPublic] = useState(true);

  const triggerWebhook = async (resourceId: string, eventType: string, customStateObj: any = null) => {
    setLoading(true);
    setAuditResult(null);
    try {
      const response = await fetch("http://localhost:8000/webhook/aws", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          event_type: eventType,
          resource_id: resourceId,
          timestamp: new Date().toISOString(),
          custom_state: customStateObj
        }),
      });
      const data = await response.json();
      setAuditResult(data);
    } catch (error) {
      console.error("Error triggering webhook:", error);
      alert("Ensure the backend is running on port 8000.");
    }
    setLoading(false);
  };

  const handleCustomSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    triggerWebhook(customResource, "custom:Deployment", {
      type: customType,
      encrypted: customEncrypted,
      public_access: customPublic
    });
  };

  return (
    <div className="min-h-screen bg-slate-50 p-8 text-slate-900 font-sans">
      <header className="mb-8 flex flex-col md:flex-row items-start md:items-center justify-between border-b pb-4 gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-slate-900">Aura</h1>
          <p className="text-slate-500 text-sm mt-1">Autonomous Unified Risk & Audit System (GraphRAG + MCP)</p>
        </div>
        <div className="flex flex-wrap gap-3">
          <button
            onClick={() => setIsCustomMode(!isCustomMode)}
            className="bg-slate-200 hover:bg-slate-300 text-slate-700 font-medium py-2 px-4 rounded-lg shadow-sm transition-all text-sm flex items-center gap-2"
          >
            {isCustomMode ? "Hide Custom Builder" : "Show Custom Builder"}
          </button>
          <button
            onClick={() => triggerWebhook("user-data-bucket", "s3:CreateBucket")}
            disabled={loading}
            className="bg-rose-600 hover:bg-rose-700 text-white font-medium py-2 px-4 rounded-lg shadow-sm transition-all disabled:opacity-50 text-sm flex items-center gap-2"
          >
            Deploy Unencrypted S3
          </button>
          <button
            onClick={() => triggerWebhook("finance-db", "rds:CreateDBInstance")}
            disabled={loading}
            className="bg-emerald-600 hover:bg-emerald-700 text-white font-medium py-2 px-4 rounded-lg shadow-sm transition-all disabled:opacity-50 text-sm flex items-center gap-2"
          >
            Deploy Secure RDS DB
          </button>
        </div>
      </header>

      {/* Custom Deployment Builder Form */}
      {isCustomMode && (
        <form onSubmit={handleCustomSubmit} className="bg-white p-5 rounded-xl shadow-sm border border-slate-200 mb-8 animate-in fade-in slide-in-from-top-4">
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <svg className="w-5 h-5 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
            Custom Deployment Webhook
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Resource Mapped in Neo4j</label>
              <select value={customResource} onChange={(e) => setCustomResource(e.target.value)} className="w-full bg-slate-50 border border-slate-300 text-slate-900 text-sm rounded-lg focus:ring-indigo-500 focus:border-indigo-500 block p-2.5">
                <option value="user-data-bucket">user-data-bucket (Governed by SOC2)</option>
                <option value="finance-db">finance-db (Governed by GDPR)</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Resource Type</label>
              <select value={customType} onChange={(e) => setCustomType(e.target.value)} className="w-full bg-slate-50 border border-slate-300 text-slate-900 text-sm rounded-lg focus:ring-indigo-500 focus:border-indigo-500 block p-2.5">
                <option value="S3">S3 Bucket</option>
                <option value="RDS">RDS Database</option>
              </select>
            </div>
            <div className="flex items-center h-10 gap-4">
              <label className="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" checked={customEncrypted} onChange={(e) => setCustomEncrypted(e.target.checked)} className="sr-only peer" />
                <div className="w-11 h-6 bg-slate-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600"></div>
                <span className="ml-3 text-sm font-medium text-slate-700">Encrypted</span>
              </label>
              <label className="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" checked={customPublic} onChange={(e) => setCustomPublic(e.target.checked)} className="sr-only peer" />
                <div className="w-11 h-6 bg-slate-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-rose-600"></div>
                <span className="ml-3 text-sm font-medium text-slate-700">Public Access</span>
              </label>
            </div>
            <div>
              <button type="submit" className="w-full text-white bg-indigo-600 hover:bg-indigo-700 focus:ring-4 focus:ring-indigo-300 font-medium rounded-lg text-sm px-5 py-2.5 transition-colors">
                Fire Custom Webhook
              </button>
            </div>
          </div>
        </form>
      )}

      {loading && (
        <div className="flex justify-center my-10">
          <div className="flex flex-col items-center gap-3">
            <svg className="animate-spin h-8 w-8 text-indigo-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
            <p className="text-sm font-medium text-slate-600">LangGraph Swarm is investigating GraphRAG...</p>
          </div>
        </div>
      )}

      {!auditResult && !loading && (
        <div className="flex flex-col items-center justify-center py-20 text-slate-400 border-2 border-dashed rounded-xl bg-white">
          <svg className="w-16 h-16 mb-4 text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg>
          <p className="text-lg">Waiting for cloud events...</p>
          <p className="text-sm mt-2">Use the buttons top right to simulate AWS deployments.</p>
        </div>
      )}

      {auditResult && !loading && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 animate-in fade-in duration-500">
          {/* Left Column: Status & Logs */}
          <div className="lg:col-span-1 space-y-6">
            <div className="bg-white p-6 rounded-xl shadow-sm border">
              <h2 className="text-lg font-semibold mb-4 border-b pb-2">Audit Summary</h2>
              <div className="space-y-4">
                <div>
                  <span className="text-sm text-slate-500 block">Resource ID</span>
                  <span className="font-medium text-slate-800">{auditResult.resource_id}</span>
                </div>
                <div>
                  <span className="text-sm text-slate-500 block">Compliance Status</span>
                  {auditResult.compliance_passed ? (
                    <span className="inline-flex items-center gap-1 text-emerald-700 bg-emerald-100 px-3 py-1 rounded-md font-bold text-sm mt-1">
                      <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"></path></svg>
                      Compliant (No Fix Needed)
                    </span>
                  ) : (
                    <span className="inline-flex items-center gap-1 text-rose-700 bg-rose-100 px-3 py-1 rounded-md font-bold text-sm mt-1">
                      <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd"></path></svg>
                      Violation Detected
                    </span>
                  )}
                </div>
                {auditResult.ticket_created && (
                  <div>
                    <span className="text-sm text-slate-500 block">Remediation Ticket</span>
                    <span className="text-indigo-700 font-bold bg-indigo-100 px-3 py-1 rounded-md inline-block mt-1">
                      {auditResult.ticket_created}
                    </span>
                  </div>
                )}
              </div>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-sm border">
              <h2 className="text-lg font-semibold mb-4 border-b pb-2">Swarm Execution Log</h2>
              <ol className="relative border-l-2 border-indigo-200 ml-3 space-y-6">
                {auditResult.agent_logs.map((log: string, idx: number) => (
                  <li key={idx} className="ml-6">
                    <span className="absolute flex items-center justify-center w-6 h-6 bg-indigo-100 rounded-full -left-[13px] ring-4 ring-white text-indigo-700 text-xs font-bold">
                      {idx + 1}
                    </span>
                    <p className="text-sm text-slate-700 bg-slate-50 p-3 rounded-lg border border-slate-100 shadow-sm leading-relaxed">{log}</p>
                  </li>
                ))}
              </ol>
            </div>
          </div>

          {/* Right Column: Code/Fixes */}
          <div className="lg:col-span-2">
            <div className="bg-slate-900 rounded-xl shadow-md overflow-hidden h-full flex flex-col border border-slate-800">
              <div className="bg-slate-800 px-5 py-3 flex items-center justify-between border-b border-slate-700">
                <h2 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
                  <svg className="w-5 h-5 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path></svg>
                  Generated Infrastructure as Code (Remediation)
                </h2>
                <span className="text-xs bg-slate-700 text-slate-300 px-2 py-1 rounded font-medium border border-slate-600">Terraform</span>
              </div>
              <div className="p-6 flex-grow overflow-auto bg-[#0d1117]">
                {auditResult.remediation_code ? (
                  <pre className="text-sm text-emerald-400 font-mono whitespace-pre-wrap leading-relaxed">
                    {auditResult.remediation_code}
                  </pre>
                ) : (
                  <div className="h-full flex flex-col items-center justify-center text-slate-500">
                    <svg className="w-16 h-16 mb-4 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    <p className="text-lg text-slate-400 font-medium">No remediation required.</p>
                    <p className="text-sm mt-1">Infrastructure is fully compliant with enterprise policy.</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
