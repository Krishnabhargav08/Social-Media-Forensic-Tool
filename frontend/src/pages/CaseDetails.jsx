import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import axios from 'axios'
import Sidebar from '../components/Sidebar'
import Card from '../components/Card'
import Button from '../components/Button'
import RiskMeter from '../components/RiskMeter'
import Input from '../components/Input'
import { FiDownload, FiSearch, FiBarChart2, FiFileText, FiShield, FiLock, FiArrowLeft } from 'react-icons/fi'

const CaseDetails = () => {
  const { caseId } = useParams()
  const navigate = useNavigate()
  const [caseData, setCaseData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [scraping, setScraping] = useState(false)
  const [analyzing, setAnalyzing] = useState(false)
  const [generatingReport, setGeneratingReport] = useState(false)
  const [showReportModal, setShowReportModal] = useState(false)
  const [reportPassword, setReportPassword] = useState('')
  const [reportId, setReportId] = useState(null)

  useEffect(() => {
    fetchCaseDetails()
  }, [caseId])

  const fetchCaseDetails = async () => {
    try {
      const response = await axios.get(`/api/cases/${caseId}`)
      setCaseData(response.data.case)
    } catch (error) {
      console.error('Failed to fetch case:', error)
      alert('Failed to load case details')
      navigate('/investigator/dashboard')
    } finally {
      setLoading(false)
    }
  }

  const handleScrapeData = async () => {
    setScraping(true)
    try {
      await axios.post(`/api/cases/${caseId}/scrape`)
      alert('Data scraped successfully!')
      fetchCaseDetails()
    } catch (error) {
      console.error('Scraping failed:', error)
      alert('Failed to scrape data: ' + (error.response?.data?.error || 'Unknown error'))
    } finally {
      setScraping(false)
    }
  }

  const handleAnalyze = async () => {
    setAnalyzing(true)
    try {
      await axios.post(`/api/cases/${caseId}/analyze`)
      alert('Analysis completed successfully!')
      fetchCaseDetails()
    } catch (error) {
      console.error('Analysis failed:', error)
      alert('Failed to analyze: ' + (error.response?.data?.error || 'Unknown error'))
    } finally {
      setAnalyzing(false)
    }
  }

  const handleGenerateReport = async (e) => {
    e.preventDefault()
    setGeneratingReport(true)
    
    try {
      const response = await axios.post('/api/reports/generate', {
        case_id: caseId,
        encryption_password: reportPassword
      })
      
      setReportId(response.data.report_id)
      alert('Report generated successfully! Use the same password to download.')
      setShowReportModal(false)
      setReportPassword('')
    } catch (error) {
      console.error('Report generation failed:', error)
      alert('Failed to generate report: ' + (error.response?.data?.error || 'Unknown error'))
    } finally {
      setGeneratingReport(false)
    }
  }

  if (loading) {
    return (
      <div className="flex">
        <Sidebar active="cases" />
        <div className="ml-64 flex-1 p-8 flex items-center justify-center">
          <div className="loading w-16 h-16 border-4 border-cyber-blue border-t-transparent rounded-full"></div>
        </div>
      </div>
    )
  }

  const analysis = caseData?.analysis_results || {}
  const hasData = caseData?.data_collected && caseData.data_collected.length > 0
  const hasAnalysis = Object.keys(analysis).length > 0

  return (
    <div className="flex min-h-screen bg-cyber-darker cyber-bg">
      <Sidebar active="cases" />
      
      <div className="ml-64 flex-1 p-8">
        {/* Header */}
        <div className="mb-8">
          <Button
            variant="secondary"
            size="sm"
            onClick={() => navigate('/investigator/dashboard')}
            icon={<FiArrowLeft />}
            className="mb-4"
          >
            Back to Dashboard
          </Button>
          
          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-4xl font-bold text-cyber-blue mb-2">
                Case: {caseData?.target_username}
              </h1>
              <p className="text-gray-400 capitalize">Platform: {caseData?.platform}</p>
              <p className="text-xs text-gray-500 mt-2 font-mono">ID: {caseData?._id}</p>
            </div>
            
            <div className="text-right">
              <span className={`
                px-4 py-2 rounded-lg font-bold text-sm inline-block
                ${caseData?.status === 'active' 
                  ? 'bg-purple-500 bg-opacity-20 text-purple-400 border-2 border-purple-500' 
                  : 'bg-green-500 bg-opacity-20 text-green-400 border-2 border-green-500'}
              `}>
                {caseData?.status?.toUpperCase()}
              </span>
            </div>
          </div>
        </div>

        <div className="grid lg:grid-cols-3 gap-6">
          {/* Left Column - Actions */}
          <div className="space-y-6">
            <Card glow>
              <h2 className="text-xl font-bold text-cyber-green mb-4">Investigation Actions</h2>
              
              <div className="space-y-3">
                <Button
                  variant="primary"
                  className="w-full"
                  onClick={handleScrapeData}
                  disabled={scraping}
                  icon={<FiSearch />}
                >
                  {scraping ? 'Scraping...' : 'Scrape Data'}
                </Button>

                <Button
                  variant="primary"
                  className="w-full"
                  onClick={handleAnalyze}
                  disabled={!hasData || analyzing}
                  icon={<FiBarChart2 />}
                >
                  {analyzing ? 'Analyzing...' : 'Analyze Data'}
                </Button>

                <Button
                  variant="success"
                  className="w-full"
                  onClick={() => setShowReportModal(true)}
                  disabled={!hasAnalysis}
                  icon={<FiFileText />}
                >
                  Generate Report
                </Button>
              </div>

              {!hasData && (
                <p className="text-xs text-gray-500 mt-4">
                  ℹ️ Start by scraping data from the target profile
                </p>
              )}
            </Card>

            {/* Evidence Hash */}
            {caseData?.evidence_hash && (
              <Card>
                <h3 className="text-sm font-bold text-cyber-blue mb-2 flex items-center gap-2">
                  <FiShield size={16} />
                  Evidence Integrity
                </h3>
                <p className="text-xs text-gray-400 mb-2">SHA-256 Hash:</p>
                <p className="font-mono text-xs text-cyber-green break-all bg-cyber-dark p-2 rounded">
                  {caseData.evidence_hash}
                </p>
              </Card>
            )}
          </div>

          {/* Middle Column - Risk Analysis */}
          <div className="space-y-6">
            <Card className="text-center">
              <h2 className="text-xl font-bold text-cyber-green mb-6">Risk Assessment</h2>
              
              {hasAnalysis ? (
                <RiskMeter score={caseData.risk_score || 0} size="lg" />
              ) : (
                <div className="py-12">
                  <p className="text-gray-400">No analysis data yet</p>
                  <p className="text-xs text-gray-500 mt-2">
                    Scrape and analyze data to see risk assessment
                  </p>
                </div>
              )}
            </Card>

            {/* Sentiment Analysis */}
            {analysis.sentiment && (
              <Card>
                <h3 className="text-lg font-bold text-cyber-blue mb-4">Sentiment Analysis</h3>
                
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-gray-400">Overall:</span>
                    <span className={`font-bold uppercase ${
                      analysis.sentiment.overall === 'positive' ? 'text-green-500' :
                      analysis.sentiment.overall === 'negative' ? 'text-red-500' :
                      'text-gray-400'
                    }`}>
                      {analysis.sentiment.overall}
                    </span>
                  </div>

                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-green-500">Positive</span>
                      <span className="text-green-500">{analysis.sentiment.positive_percentage}%</span>
                    </div>
                    <div className="w-full bg-gray-700 rounded-full h-2">
                      <div className="bg-green-500 h-2 rounded-full" style={{ width: `${analysis.sentiment.positive_percentage}%` }} />
                    </div>
                  </div>

                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-red-500">Negative</span>
                      <span className="text-red-500">{analysis.sentiment.negative_percentage}%</span>
                    </div>
                    <div className="w-full bg-gray-700 rounded-full h-2">
                      <div className="bg-red-500 h-2 rounded-full" style={{ width: `${analysis.sentiment.negative_percentage}%` }} />
                    </div>
                  </div>

                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-gray-400">Neutral</span>
                      <span className="text-gray-400">{analysis.sentiment.neutral_percentage}%</span>
                    </div>
                    <div className="w-full bg-gray-700 rounded-full h-2">
                      <div className="bg-gray-400 h-2 rounded-full" style={{ width: `${analysis.sentiment.neutral_percentage}%` }} />
                    </div>
                  </div>
                </div>
              </Card>
            )}
          </div>

          {/* Right Column - Detection Results */}
          <div className="space-y-6">
            {/* Cyberbullying Detection */}
            {analysis.cyberbullying && (
              <Card className={analysis.cyberbullying.detected ? 'border-2 border-red-500' : ''}>
                <h3 className="text-lg font-bold text-cyber-blue mb-4">Cyberbullying Detection</h3>
                
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-gray-400">Status:</span>
                    <span className={`font-bold ${analysis.cyberbullying.detected ? 'text-red-500' : 'text-green-500'}`}>
                      {analysis.cyberbullying.detected ? 'DETECTED' : 'NOT DETECTED'}
                    </span>
                  </div>

                  <div className="flex justify-between items-center">
                    <span className="text-gray-400">Confidence:</span>
                    <span className="font-bold text-white">{analysis.cyberbullying.confidence}%</span>
                  </div>

                  <div className="flex justify-between items-center">
                    <span className="text-gray-400">Incidents:</span>
                    <span className="font-bold text-white">{analysis.cyberbullying.incidents_count}</span>
                  </div>
                </div>
              </Card>
            )}

            {/* Fraud Detection */}
            {analysis.fraud_detection && (
              <Card className={analysis.fraud_detection.detected ? 'border-2 border-orange-500' : ''}>
                <h3 className="text-lg font-bold text-cyber-blue mb-4">Fraud Detection</h3>
                
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-gray-400">Status:</span>
                    <span className={`font-bold ${analysis.fraud_detection.detected ? 'text-orange-500' : 'text-green-500'}`}>
                      {analysis.fraud_detection.detected ? 'DETECTED' : 'NOT DETECTED'}
                    </span>
                  </div>

                  <div className="flex justify-between items-center">
                    <span className="text-gray-400">Confidence:</span>
                    <span className="font-bold text-white">{analysis.fraud_detection.confidence}%</span>
                  </div>

                  <div className="flex justify-between items-center">
                    <span className="text-gray-400">Suspicious Posts:</span>
                    <span className="font-bold text-white">{analysis.fraud_detection.suspicious_count}</span>
                  </div>
                </div>
              </Card>
            )}

            {/* Fake Profile */}
            {analysis.fake_profile && (
              <Card className={analysis.fake_profile.is_potentially_fake ? 'border-2 border-yellow-500' : ''}>
                <h3 className="text-lg font-bold text-cyber-blue mb-4">Fake Profile Analysis</h3>
                
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-gray-400">Status:</span>
                    <span className={`font-bold ${analysis.fake_profile.is_potentially_fake ? 'text-yellow-500' : 'text-green-500'}`}>
                      {analysis.fake_profile.is_potentially_fake ? 'POTENTIALLY FAKE' : 'GENUINE'}
                    </span>
                  </div>

                  <div className="flex justify-between items-center">
                    <span className="text-gray-400">Fake Score:</span>
                    <span className="font-bold text-white">{analysis.fake_profile.fake_score}/100</span>
                  </div>

                  <div className="flex justify-between items-center">
                    <span className="text-gray-400">Account Age:</span>
                    <span className="font-bold text-white">{analysis.fake_profile.account_age_days} days</span>
                  </div>

                  {analysis.fake_profile.risk_factors && analysis.fake_profile.risk_factors.length > 0 && (
                    <div className="mt-4">
                      <p className="text-xs text-gray-400 mb-2">Risk Factors:</p>
                      <ul className="text-xs text-yellow-500 space-y-1">
                        {analysis.fake_profile.risk_factors.map((factor, idx) => (
                          <li key={idx}>• {factor}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </Card>
            )}
          </div>
        </div>
      </div>

      {/* Report Generation Modal */}
      {showReportModal && (
        <div className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50 p-6">
          <div className="glass rounded-lg p-8 max-w-md w-full border-2 border-cyber-blue">
            <h2 className="text-2xl font-bold text-cyber-blue mb-6 flex items-center gap-3">
              <FiLock size={24} />
              Generate Encrypted Report
            </h2>
            
            <p className="text-gray-300 mb-6">
              Set a password to encrypt this forensic report. You will need this password to download and view the report.
            </p>

            <form onSubmit={handleGenerateReport} className="space-y-4">
              <Input
                label="Encryption Password"
                type="password"
                value={reportPassword}
                onChange={(e) => setReportPassword(e.target.value)}
                placeholder="Enter a strong password"
                icon={<FiLock />}
                required
              />

              <div className="bg-yellow-500 bg-opacity-10 border border-yellow-500 rounded-lg p-3">
                <p className="text-yellow-500 text-xs">
                  ⚠️ Remember this password! It cannot be recovered and is required to decrypt the report.
                </p>
              </div>

              <div className="flex gap-3 pt-4">
                <Button
                  type="submit"
                  variant="success"
                  className="flex-1"
                  disabled={generatingReport}
                >
                  {generatingReport ? 'Generating...' : 'Generate Report'}
                </Button>
                
                <Button
                  type="button"
                  variant="secondary"
                  onClick={() => {
                    setShowReportModal(false)
                    setReportPassword('')
                  }}
                  className="flex-1"
                >
                  Cancel
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

export default CaseDetails
