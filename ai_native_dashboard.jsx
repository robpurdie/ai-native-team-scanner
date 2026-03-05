import React, { useState, useMemo } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { ChevronDown, ChevronUp, TrendingUp, TrendingDown, AlertCircle, CheckCircle, MinusCircle } from 'lucide-react';

// Mock data generator based on test cases
const generateMockTeams = () => {
  return [
    // TC-01: Clear L2 Team
    {
      id: 'team-001',
      name: 'Platform Engineering Squad',
      domain: 'Infrastructure',
      activeContributors: 6,
      signals: {
        aiAdoption: {
          configFiles: { value: 65, threshold_l1: 10, threshold_l2: 10, met_l1: true, met_l2: true, label: 'AI config files (lines)' },
          dependencies: { value: 3, threshold_l1: 1, threshold_l2: 2, met_l1: true, met_l2: true, label: 'AI dependencies' },
          prRichness: { value: 420, threshold_l1: 150, threshold_l2: 300, spread: 0.83, spread_threshold_l1: 0.50, spread_threshold_l2: 0.80, met_l1: true, met_l2: true, label: 'PR description richness (chars)' },
          orchestration: { value: true, threshold_l2: true, met_l1: true, met_l2: true, label: 'AI orchestration present' }
        },
        engineeringPractices: {
          commitFreq: { value: 5.8, threshold_l1: 3, threshold_l2: 5, met_l1: true, met_l2: true, label: 'Commits/contributor/week' },
          prSize: { value: 165, threshold_l1: 400, threshold_l2: 200, met_l1: true, met_l2: true, label: 'Median PR size (lines)' },
          testSpread: { value: 0.67, threshold_l1: 0.01, threshold_l2: 0.60, met_l1: true, met_l2: true, label: 'Test contributor spread' },
          cicd: { value: true, threshold_l1: true, threshold_l2: true, met_l1: true, met_l2: true, label: 'CI/CD with tests' },
          docCurrency: { value: 0.12, threshold_l1: 0.05, threshold_l2: 0.10, met_l1: true, met_l2: true, label: 'Documentation currency' }
        }
      },
      sustainedPattern: true,
      repoAge: 420
    },
    
    // TC-02: Solid L1 Team
    {
      id: 'team-002',
      name: 'Checkout Services',
      domain: 'Commerce',
      activeContributors: 4,
      signals: {
        aiAdoption: {
          configFiles: { value: 25, threshold_l1: 10, threshold_l2: 10, met_l1: true, met_l2: true, label: 'AI config files (lines)' },
          dependencies: { value: 2, threshold_l1: 1, threshold_l2: 2, met_l1: true, met_l2: true, label: 'AI dependencies' },
          prRichness: { value: 325, threshold_l1: 150, threshold_l2: 300, spread: 0.75, spread_threshold_l1: 0.50, spread_threshold_l2: 0.80, met_l1: true, met_l2: false, label: 'PR description richness (chars)' },
          orchestration: { value: false, threshold_l2: true, met_l1: true, met_l2: false, label: 'AI orchestration present' }
        },
        engineeringPractices: {
          commitFreq: { value: 4.5, threshold_l1: 3, threshold_l2: 5, met_l1: true, met_l2: false, label: 'Commits/contributor/week' },
          prSize: { value: 280, threshold_l1: 400, threshold_l2: 200, met_l1: true, met_l2: false, label: 'Median PR size (lines)' },
          testSpread: { value: 0.50, threshold_l1: 0.01, threshold_l2: 0.60, met_l1: true, met_l2: false, label: 'Test contributor spread' },
          cicd: { value: true, threshold_l1: true, threshold_l2: true, met_l1: true, met_l2: true, label: 'CI/CD with tests' },
          docCurrency: { value: 0.07, threshold_l1: 0.05, threshold_l2: 0.10, met_l1: true, met_l2: false, label: 'Documentation currency' }
        }
      },
      sustainedPattern: false,
      repoAge: 420
    },
    
    // TC-03: Classic L0 Team
    {
      id: 'team-003',
      name: 'Legacy Migration',
      domain: 'Platform',
      activeContributors: 5,
      signals: {
        aiAdoption: {
          configFiles: { value: 0, threshold_l1: 10, threshold_l2: 10, met_l1: false, met_l2: false, label: 'AI config files (lines)' },
          dependencies: { value: 0, threshold_l1: 1, threshold_l2: 2, met_l1: false, met_l2: false, label: 'AI dependencies' },
          prRichness: { value: 85, threshold_l1: 150, threshold_l2: 300, spread: 0.40, spread_threshold_l1: 0.50, spread_threshold_l2: 0.80, met_l1: false, met_l2: false, label: 'PR description richness (chars)' },
          orchestration: { value: false, threshold_l2: true, met_l1: false, met_l2: false, label: 'AI orchestration present' }
        },
        engineeringPractices: {
          commitFreq: { value: 2.8, threshold_l1: 3, threshold_l2: 5, met_l1: false, met_l2: false, label: 'Commits/contributor/week' },
          prSize: { value: 520, threshold_l1: 400, threshold_l2: 200, met_l1: false, met_l2: false, label: 'Median PR size (lines)' },
          testSpread: { value: 0.20, threshold_l1: 0.01, threshold_l2: 0.60, met_l1: true, met_l2: false, label: 'Test contributor spread' },
          cicd: { value: false, threshold_l1: true, threshold_l2: true, met_l1: false, met_l2: false, label: 'CI/CD with tests' },
          docCurrency: { value: 0.02, threshold_l1: 0.05, threshold_l2: 0.10, met_l1: false, met_l2: false, label: 'Documentation currency' }
        }
      },
      sustainedPattern: false,
      repoAge: 420
    },
    
    // TC-04: High AI, Weak Engineering (Cargo Cult)
    {
      id: 'team-004',
      name: 'Innovation Lab',
      domain: 'R&D',
      activeContributors: 4,
      signals: {
        aiAdoption: {
          configFiles: { value: 45, threshold_l1: 10, threshold_l2: 10, met_l1: true, met_l2: true, label: 'AI config files (lines)' },
          dependencies: { value: 3, threshold_l1: 1, threshold_l2: 2, met_l1: true, met_l2: true, label: 'AI dependencies' },
          prRichness: { value: 380, threshold_l1: 150, threshold_l2: 300, spread: 0.75, spread_threshold_l1: 0.50, spread_threshold_l2: 0.80, met_l1: true, met_l2: false, label: 'PR description richness (chars)' },
          orchestration: { value: false, threshold_l2: true, met_l1: true, met_l2: false, label: 'AI orchestration present' }
        },
        engineeringPractices: {
          commitFreq: { value: 2.2, threshold_l1: 3, threshold_l2: 5, met_l1: false, met_l2: false, label: 'Commits/contributor/week' },
          prSize: { value: 680, threshold_l1: 400, threshold_l2: 200, met_l1: false, met_l2: false, label: 'Median PR size (lines)' },
          testSpread: { value: 0.00, threshold_l1: 0.01, threshold_l2: 0.60, met_l1: false, met_l2: false, label: 'Test contributor spread' },
          cicd: { value: false, threshold_l1: true, threshold_l2: true, met_l1: false, met_l2: false, label: 'CI/CD with tests' },
          docCurrency: { value: 0.01, threshold_l1: 0.05, threshold_l2: 0.10, met_l1: false, met_l2: false, label: 'Documentation currency' }
        }
      },
      sustainedPattern: false,
      repoAge: 420,
      note: 'Cargo cult AI adoption - tools without discipline'
    },
    
    // TC-05: Strong Engineering, Minimal AI
    {
      id: 'team-005',
      name: 'Core Services',
      domain: 'Platform',
      activeContributors: 5,
      signals: {
        aiAdoption: {
          configFiles: { value: 0, threshold_l1: 10, threshold_l2: 10, met_l1: false, met_l2: false, label: 'AI config files (lines)' },
          dependencies: { value: 0, threshold_l1: 1, threshold_l2: 2, met_l1: false, met_l2: false, label: 'AI dependencies' },
          prRichness: { value: 210, threshold_l1: 150, threshold_l2: 300, spread: 0.60, spread_threshold_l1: 0.50, spread_threshold_l2: 0.80, met_l1: true, met_l2: false, label: 'PR description richness (chars)' },
          orchestration: { value: false, threshold_l2: true, met_l1: false, met_l2: false, label: 'AI orchestration present' }
        },
        engineeringPractices: {
          commitFreq: { value: 6.2, threshold_l1: 3, threshold_l2: 5, met_l1: true, met_l2: true, label: 'Commits/contributor/week' },
          prSize: { value: 145, threshold_l1: 400, threshold_l2: 200, met_l1: true, met_l2: true, label: 'Median PR size (lines)' },
          testSpread: { value: 0.80, threshold_l1: 0.01, threshold_l2: 0.60, met_l1: true, met_l2: true, label: 'Test contributor spread' },
          cicd: { value: true, threshold_l1: true, threshold_l2: true, met_l1: true, met_l2: true, label: 'CI/CD with tests' },
          docCurrency: { value: 0.11, threshold_l1: 0.05, threshold_l2: 0.10, met_l1: true, met_l2: true, label: 'Documentation currency' }
        }
      },
      sustainedPattern: true,
      repoAge: 420,
      note: 'Excellent engineering foundation, ready for AI enablement'
    },
    
    // TC-15: Borderline L1/L2 (Near miss)
    {
      id: 'team-006',
      name: 'Data Platform',
      domain: 'Analytics',
      activeContributors: 5,
      signals: {
        aiAdoption: {
          configFiles: { value: 38, threshold_l1: 10, threshold_l2: 10, met_l1: true, met_l2: true, label: 'AI config files (lines)' },
          dependencies: { value: 2, threshold_l1: 1, threshold_l2: 2, met_l1: true, met_l2: true, label: 'AI dependencies' },
          prRichness: { value: 340, threshold_l1: 150, threshold_l2: 300, spread: 0.82, spread_threshold_l1: 0.50, spread_threshold_l2: 0.80, met_l1: true, met_l2: true, label: 'PR description richness (chars)' },
          orchestration: { value: true, threshold_l2: true, met_l1: true, met_l2: true, label: 'AI orchestration present' }
        },
        engineeringPractices: {
          commitFreq: { value: 4.2, threshold_l1: 3, threshold_l2: 5, met_l1: true, met_l2: false, label: 'Commits/contributor/week' },
          prSize: { value: 180, threshold_l1: 400, threshold_l2: 200, met_l1: true, met_l2: true, label: 'Median PR size (lines)' },
          testSpread: { value: 0.60, threshold_l1: 0.01, threshold_l2: 0.60, met_l1: true, met_l2: true, label: 'Test contributor spread' },
          cicd: { value: true, threshold_l1: true, threshold_l2: true, met_l1: true, met_l2: true, label: 'CI/CD with tests' },
          docCurrency: { value: 0.08, threshold_l1: 0.05, threshold_l2: 0.10, met_l1: true, met_l2: false, label: 'Documentation currency' }
        }
      },
      sustainedPattern: true,
      repoAge: 420,
      note: 'Near L2 - 2 gaps remaining'
    },
    
    // TC-18: Improvement Trajectory
    {
      id: 'team-007',
      name: 'Mobile Apps',
      domain: 'Consumer',
      activeContributors: 6,
      signals: {
        aiAdoption: {
          configFiles: { value: 52, threshold_l1: 10, threshold_l2: 10, met_l1: true, met_l2: true, label: 'AI config files (lines)' },
          dependencies: { value: 2, threshold_l1: 1, threshold_l2: 2, met_l1: true, met_l2: true, label: 'AI dependencies' },
          prRichness: { value: 360, threshold_l1: 150, threshold_l2: 300, spread: 0.81, spread_threshold_l1: 0.50, spread_threshold_l2: 0.80, met_l1: true, met_l2: true, label: 'PR description richness (chars)' },
          orchestration: { value: true, threshold_l2: true, met_l1: true, met_l2: true, label: 'AI orchestration present' }
        },
        engineeringPractices: {
          commitFreq: { value: 5.3, threshold_l1: 3, threshold_l2: 5, met_l1: true, met_l2: true, label: 'Commits/contributor/week' },
          prSize: { value: 175, threshold_l1: 400, threshold_l2: 200, met_l1: true, met_l2: true, label: 'Median PR size (lines)' },
          testSpread: { value: 0.72, threshold_l1: 0.01, threshold_l2: 0.60, met_l1: true, met_l2: true, label: 'Test contributor spread' },
          cicd: { value: true, threshold_l1: true, threshold_l2: true, met_l1: true, met_l2: true, label: 'CI/CD with tests' },
          docCurrency: { value: 0.13, threshold_l1: 0.05, threshold_l2: 0.10, met_l1: true, met_l2: true, label: 'Documentation currency' }
        }
      },
      sustainedPattern: true,
      repoAge: 420,
      trajectory: 'L0 → L1 → L2',
      note: 'Sustained improvement over 3 quarters'
    },
    
    // TC-17: Partial History
    {
      id: 'team-008',
      name: 'Security Tooling',
      domain: 'Security',
      activeContributors: 4,
      signals: {
        aiAdoption: {
          configFiles: { value: 41, threshold_l1: 10, threshold_l2: 10, met_l1: true, met_l2: true, label: 'AI config files (lines)' },
          dependencies: { value: 2, threshold_l1: 1, threshold_l2: 2, met_l1: true, met_l2: true, label: 'AI dependencies' },
          prRichness: { value: 315, threshold_l1: 150, threshold_l2: 300, spread: 0.85, spread_threshold_l1: 0.50, spread_threshold_l2: 0.80, met_l1: true, met_l2: true, label: 'PR description richness (chars)' },
          orchestration: { value: true, threshold_l2: true, met_l1: true, met_l2: true, label: 'AI orchestration present' }
        },
        engineeringPractices: {
          commitFreq: { value: 5.1, threshold_l1: 3, threshold_l2: 5, met_l1: true, met_l2: true, label: 'Commits/contributor/week' },
          prSize: { value: 185, threshold_l1: 400, threshold_l2: 200, met_l1: true, met_l2: true, label: 'Median PR size (lines)' },
          testSpread: { value: 0.68, threshold_l1: 0.01, threshold_l2: 0.60, met_l1: true, met_l2: true, label: 'Test contributor spread' },
          cicd: { value: true, threshold_l1: true, threshold_l2: true, met_l1: true, met_l2: true, label: 'CI/CD with tests' },
          docCurrency: { value: 0.11, threshold_l1: 0.05, threshold_l2: 0.10, met_l1: true, met_l2: true, label: 'Documentation currency' }
        }
      },
      sustainedPattern: false,
      repoAge: 150,
      note: 'Insufficient history for L2 - single window only'
    }
  ];
};

// Scoring engine
const calculateScore = (team) => {
  const { signals, sustainedPattern, repoAge } = team;
  
  // Check AI Adoption dimension
  const aiL1Met = (
    signals.aiAdoption.configFiles.met_l1 &&
    signals.aiAdoption.dependencies.met_l1 &&
    signals.aiAdoption.prRichness.met_l1
  );
  
  const aiL2Met = (
    aiL1Met &&
    signals.aiAdoption.configFiles.met_l2 &&
    signals.aiAdoption.dependencies.met_l2 &&
    signals.aiAdoption.prRichness.met_l2 &&
    signals.aiAdoption.orchestration.met_l2 &&
    sustainedPattern &&
    repoAge >= 180
  );
  
  const aiLevel = aiL2Met ? 2 : aiL1Met ? 1 : 0;
  
  // Check Engineering Practices dimension
  const engL1Met = (
    signals.engineeringPractices.commitFreq.met_l1 &&
    signals.engineeringPractices.prSize.met_l1 &&
    signals.engineeringPractices.testSpread.met_l1
  );
  
  const engL2Met = (
    engL1Met &&
    signals.engineeringPractices.commitFreq.met_l2 &&
    signals.engineeringPractices.prSize.met_l2 &&
    signals.engineeringPractices.testSpread.met_l2 &&
    signals.engineeringPractices.cicd.met_l2 &&
    signals.engineeringPractices.docCurrency.met_l2 &&
    sustainedPattern &&
    repoAge >= 180
  );
  
  const engLevel = engL2Met ? 2 : engL1Met ? 1 : 0;
  
  // Overall level is lower of two dimensions
  const overallLevel = Math.min(aiLevel, engLevel);
  
  return {
    overall: overallLevel,
    aiAdoption: aiLevel,
    engineeringPractices: engLevel,
    aiL1Met,
    aiL2Met,
    engL1Met,
    engL2Met
  };
};

// Gap analysis
const analyzeGaps = (team, score) => {
  const gaps = [];
  const { signals } = team;
  
  // Target next level
  const targetLevel = score.overall < 2 ? score.overall + 1 : 2;
  
  // Check AI Adoption gaps
  Object.entries(signals.aiAdoption).forEach(([key, signal]) => {
    if (targetLevel === 1 && !signal.met_l1) {
      gaps.push({
        dimension: 'AI Adoption',
        signal: signal.label,
        current: signal.value,
        required: signal.threshold_l1,
        delta: calculateDelta(signal, 'l1'),
        priority: 'high'
      });
    } else if (targetLevel === 2 && !signal.met_l2) {
      gaps.push({
        dimension: 'AI Adoption',
        signal: signal.label,
        current: signal.value,
        required: signal.threshold_l2,
        delta: calculateDelta(signal, 'l2'),
        priority: determinePriority(key)
      });
    }
  });
  
  // Check Engineering Practices gaps
  Object.entries(signals.engineeringPractices).forEach(([key, signal]) => {
    if (targetLevel === 1 && !signal.met_l1) {
      gaps.push({
        dimension: 'Engineering Practices',
        signal: signal.label,
        current: signal.value,
        required: signal.threshold_l1,
        delta: calculateDelta(signal, 'l1'),
        priority: 'high'
      });
    } else if (targetLevel === 2 && !signal.met_l2) {
      gaps.push({
        dimension: 'Engineering Practices',
        signal: signal.label,
        current: signal.value,
        required: signal.threshold_l2,
        delta: calculateDelta(signal, 'l2'),
        priority: determinePriority(key)
      });
    }
  });
  
  return gaps.sort((a, b) => {
    const priorityOrder = { high: 0, medium: 1, low: 2 };
    return priorityOrder[a.priority] - priorityOrder[b.priority];
  });
};

const calculateDelta = (signal, level) => {
  const threshold = level === 'l1' ? signal.threshold_l1 : signal.threshold_l2;
  
  if (typeof signal.value === 'boolean') {
    return signal.value ? 'Met' : 'Not detected';
  }
  
  // For PR size, smaller is better
  if (signal.label.includes('PR size')) {
    return signal.value > threshold ? `${signal.value - threshold} lines over` : 'Met';
  }
  
  // For percentages
  if (signal.label.includes('spread') || signal.label.includes('currency')) {
    return `${((threshold - signal.value) * 100).toFixed(0)}% gap`;
  }
  
  // For counts
  return `${(threshold - signal.value).toFixed(1)} gap`;
};

const determinePriority = (key) => {
  const highPriority = ['commitFreq', 'prSize', 'configFiles'];
  const mediumPriority = ['testSpread', 'docCurrency', 'dependencies'];
  
  if (highPriority.includes(key)) return 'high';
  if (mediumPriority.includes(key)) return 'medium';
  return 'low';
};

// Main Dashboard Component
export default function AITeamDashboard() {
  const [selectedTeam, setSelectedTeam] = useState(null);
  const [filterLevel, setFilterLevel] = useState('all');
  const [sortBy, setSortBy] = useState('name');
  
  const teams = useMemo(() => generateMockTeams(), []);
  
  const teamsWithScores = useMemo(() => {
    return teams.map(team => ({
      ...team,
      score: calculateScore(team),
      gaps: null // Computed on demand
    }));
  }, [teams]);
  
  const filteredTeams = useMemo(() => {
    let filtered = teamsWithScores;
    
    if (filterLevel !== 'all') {
      const level = parseInt(filterLevel);
      filtered = filtered.filter(t => t.score.overall === level);
    }
    
    // Sort
    filtered.sort((a, b) => {
      if (sortBy === 'name') return a.name.localeCompare(b.name);
      if (sortBy === 'level') return b.score.overall - a.score.overall;
      if (sortBy === 'domain') return a.domain.localeCompare(b.domain);
      return 0;
    });
    
    return filtered;
  }, [teamsWithScores, filterLevel, sortBy]);
  
  const distribution = useMemo(() => {
    const dist = { l0: 0, l1: 0, l2: 0 };
    teamsWithScores.forEach(t => {
      if (t.score.overall === 0) dist.l0++;
      else if (t.score.overall === 1) dist.l1++;
      else dist.l2++;
    });
    return [
      { name: 'L0: Not Yet', count: dist.l0, level: 0 },
      { name: 'L1: Integrating', count: dist.l1, level: 1 },
      { name: 'L2: AI-Native', count: dist.l2, level: 2 }
    ];
  }, [teamsWithScores]);
  
  const selectedTeamWithGaps = useMemo(() => {
    if (!selectedTeam) return null;
    const team = teamsWithScores.find(t => t.id === selectedTeam);
    if (!team) return null;
    return {
      ...team,
      gaps: analyzeGaps(team, team.score)
    };
  }, [selectedTeam, teamsWithScores]);
  
  return (
    <div className="min-h-screen bg-slate-50 font-sans">
      {/* Header */}
      <div className="bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
        <div className="max-w-7xl mx-auto px-6 py-12">
          <div className="flex items-start justify-between">
            <div>
              <h1 className="text-4xl font-bold tracking-tight mb-2">
                AI-Native Team Detection
              </h1>
              <p className="text-slate-300 text-lg max-w-2xl">
                Identifying teams demonstrating sustained AI adoption paired with engineering discipline
              </p>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-lg px-6 py-4 border border-white/20">
              <div className="text-sm text-slate-300 mb-1">Total Teams Analyzed</div>
              <div className="text-3xl font-bold">{teams.length}</div>
            </div>
          </div>
        </div>
      </div>
      
      {/* Distribution Overview */}
      <div className="max-w-7xl mx-auto px-6 -mt-8 mb-8">
        <div className="bg-white rounded-xl shadow-lg border border-slate-200 p-6">
          <h2 className="text-xl font-bold text-slate-900 mb-4">Distribution</h2>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={distribution}>
              <XAxis dataKey="name" stroke="#64748b" />
              <YAxis stroke="#64748b" />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#1e293b', 
                  border: 'none', 
                  borderRadius: '8px',
                  color: '#fff'
                }}
              />
              <Bar dataKey="count" radius={[8, 8, 0, 0]}>
                {distribution.map((entry, index) => (
                  <Cell 
                    key={`cell-${index}`}
                    fill={entry.level === 2 ? '#10b981' : entry.level === 1 ? '#f59e0b' : '#94a3b8'}
                  />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
          
          <div className="mt-6 grid grid-cols-3 gap-4">
            {distribution.map((item) => (
              <div 
                key={item.name}
                className="text-center p-4 rounded-lg bg-slate-50"
              >
                <div className="text-3xl font-bold text-slate-900">{item.count}</div>
                <div className="text-sm text-slate-600 mt-1">{item.name}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
      
      {/* Filters */}
      <div className="max-w-7xl mx-auto px-6 mb-6">
        <div className="flex gap-4 items-center">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">
              Filter by Level
            </label>
            <select
              value={filterLevel}
              onChange={(e) => setFilterLevel(e.target.value)}
              className="px-4 py-2 bg-white border border-slate-300 rounded-lg text-slate-900 focus:outline-none focus:ring-2 focus:ring-slate-400"
            >
              <option value="all">All Levels</option>
              <option value="2">L2: AI-Native</option>
              <option value="1">L1: Integrating</option>
              <option value="0">L0: Not Yet</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">
              Sort by
            </label>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-4 py-2 bg-white border border-slate-300 rounded-lg text-slate-900 focus:outline-none focus:ring-2 focus:ring-slate-400"
            >
              <option value="name">Team Name</option>
              <option value="level">Level (High to Low)</option>
              <option value="domain">Domain</option>
            </select>
          </div>
        </div>
      </div>
      
      {/* Teams Grid */}
      <div className="max-w-7xl mx-auto px-6 pb-12">
        <div className="grid grid-cols-1 gap-4">
          {filteredTeams.map((team) => (
            <TeamCard
              key={team.id}
              team={team}
              isSelected={selectedTeam === team.id}
              onSelect={() => setSelectedTeam(selectedTeam === team.id ? null : team.id)}
            />
          ))}
        </div>
      </div>
      
      {/* Detail Panel */}
      {selectedTeamWithGaps && (
        <DetailPanel
          team={selectedTeamWithGaps}
          onClose={() => setSelectedTeam(null)}
        />
      )}
    </div>
  );
}

// Team Card Component
function TeamCard({ team, isSelected, onSelect }) {
  const { name, domain, activeContributors, score, note, trajectory } = team;
  
  const levelConfig = {
    0: { label: 'L0: Not Yet', color: 'bg-slate-100 text-slate-700', border: 'border-slate-300' },
    1: { label: 'L1: Integrating', color: 'bg-amber-100 text-amber-800', border: 'border-amber-300' },
    2: { label: 'L2: AI-Native', color: 'bg-emerald-100 text-emerald-800', border: 'border-emerald-300' }
  };
  
  const config = levelConfig[score.overall];
  
  return (
    <div
      onClick={onSelect}
      className={`
        bg-white rounded-lg border-2 p-5 cursor-pointer transition-all
        ${isSelected ? 'border-slate-900 shadow-lg' : 'border-slate-200 hover:border-slate-400 shadow'}
      `}
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-2">
            <h3 className="text-lg font-bold text-slate-900">{name}</h3>
            <span className="text-sm text-slate-500">{domain}</span>
          </div>
          
          <div className="flex items-center gap-4 mb-3">
            <span className={`px-3 py-1 rounded-full text-sm font-semibold ${config.color}`}>
              {config.label}
            </span>
            <span className="text-sm text-slate-600">
              {activeContributors} active contributors
            </span>
            {trajectory && (
              <span className="text-sm text-emerald-600 font-medium flex items-center gap-1">
                <TrendingUp size={14} />
                {trajectory}
              </span>
            )}
          </div>
          
          {note && (
            <div className="text-sm text-slate-600 italic">
              {note}
            </div>
          )}
        </div>
        
        <div className="flex items-center gap-2">
          <DimensionBadge level={score.aiAdoption} label="AI" />
          <DimensionBadge level={score.engineeringPractices} label="Eng" />
          {isSelected ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
        </div>
      </div>
      
      {isSelected && (
        <div className="mt-4 pt-4 border-t border-slate-200 text-sm text-slate-600">
          Click to view detailed gap analysis →
        </div>
      )}
    </div>
  );
}

// Dimension Badge
function DimensionBadge({ level, label }) {
  const colors = {
    0: 'bg-slate-200 text-slate-700',
    1: 'bg-amber-200 text-amber-800',
    2: 'bg-emerald-200 text-emerald-800'
  };
  
  return (
    <div className={`px-2 py-1 rounded text-xs font-semibold ${colors[level]}`}>
      {label} L{level}
    </div>
  );
}

// Detail Panel Component
function DetailPanel({ team, onClose }) {
  const { name, score, gaps, signals } = team;
  
  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-6">
      <div className="bg-white rounded-xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-auto">
        {/* Header */}
        <div className="sticky top-0 bg-gradient-to-r from-slate-900 to-slate-800 text-white px-6 py-5 flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold">{name}</h2>
            <p className="text-slate-300 mt-1">Detailed Analysis & Gap Report</p>
          </div>
          <button
            onClick={onClose}
            className="text-white hover:bg-white/10 rounded-lg p-2 transition-colors"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        {/* Content */}
        <div className="p-6">
          {/* Score Summary */}
          <div className="mb-8">
            <h3 className="text-lg font-bold text-slate-900 mb-4">Overall Score</h3>
            <div className="grid grid-cols-3 gap-4">
              <ScoreCard
                title="Overall Level"
                level={score.overall}
                description="Lower of two dimensions"
              />
              <ScoreCard
                title="AI Adoption"
                level={score.aiAdoption}
                description="Tools & integration"
              />
              <ScoreCard
                title="Engineering Practices"
                level={score.engineeringPractices}
                description="Discipline & quality"
              />
            </div>
          </div>
          
          {/* Gap Analysis */}
          {gaps.length > 0 && (
            <div className="mb-8">
              <h3 className="text-lg font-bold text-slate-900 mb-4">
                Gaps to Level {score.overall + 1}
              </h3>
              <div className="space-y-3">
                {gaps.map((gap, idx) => (
                  <GapCard key={idx} gap={gap} />
                ))}
              </div>
            </div>
          )}
          
          {score.overall === 2 && gaps.length === 0 && (
            <div className="bg-emerald-50 border border-emerald-200 rounded-lg p-4 flex items-start gap-3 mb-8">
              <CheckCircle className="text-emerald-600 mt-0.5" size={20} />
              <div>
                <div className="font-semibold text-emerald-900">L2 AI-Native Team</div>
                <div className="text-sm text-emerald-700 mt-1">
                  This team demonstrates sustained AI-native working patterns. No gaps identified.
                </div>
              </div>
            </div>
          )}
          
          {/* Signals Detail */}
          <div>
            <h3 className="text-lg font-bold text-slate-900 mb-4">Signal Details</h3>
            
            <div className="mb-6">
              <h4 className="font-semibold text-slate-700 mb-3">AI Adoption Dimension</h4>
              <div className="space-y-2">
                {Object.entries(signals.aiAdoption).map(([key, signal]) => (
                  <SignalRow key={key} signal={signal} targetLevel={score.overall < 2 ? score.overall + 1 : 2} />
                ))}
              </div>
            </div>
            
            <div>
              <h4 className="font-semibold text-slate-700 mb-3">Engineering Practices Dimension</h4>
              <div className="space-y-2">
                {Object.entries(signals.engineeringPractices).map(([key, signal]) => (
                  <SignalRow key={key} signal={signal} targetLevel={score.overall < 2 ? score.overall + 1 : 2} />
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// Score Card
function ScoreCard({ title, level, description }) {
  const colors = {
    0: 'from-slate-500 to-slate-600',
    1: 'from-amber-500 to-amber-600',
    2: 'from-emerald-500 to-emerald-600'
  };
  
  return (
    <div className={`bg-gradient-to-br ${colors[level]} rounded-lg p-4 text-white`}>
      <div className="text-sm opacity-90 mb-1">{title}</div>
      <div className="text-3xl font-bold mb-1">L{level}</div>
      <div className="text-xs opacity-75">{description}</div>
    </div>
  );
}

// Gap Card
function GapCard({ gap }) {
  const priorityConfig = {
    high: { color: 'bg-red-50 border-red-200 text-red-900', icon: AlertCircle, iconColor: 'text-red-600' },
    medium: { color: 'bg-amber-50 border-amber-200 text-amber-900', icon: MinusCircle, iconColor: 'text-amber-600' },
    low: { color: 'bg-blue-50 border-blue-200 text-blue-900', icon: MinusCircle, iconColor: 'text-blue-600' }
  };
  
  const config = priorityConfig[gap.priority];
  const Icon = config.icon;
  
  return (
    <div className={`border rounded-lg p-4 ${config.color}`}>
      <div className="flex items-start gap-3">
        <Icon className={`${config.iconColor} mt-0.5`} size={20} />
        <div className="flex-1">
          <div className="font-semibold mb-1">{gap.signal}</div>
          <div className="text-sm opacity-75">
            Current: {formatValue(gap.current)} → Required: {formatValue(gap.required)}
          </div>
          <div className="text-sm font-medium mt-1">
            Gap: {gap.delta}
          </div>
        </div>
        <div className="text-xs uppercase font-semibold px-2 py-1 bg-white/50 rounded">
          {gap.priority}
        </div>
      </div>
    </div>
  );
}

// Signal Row
function SignalRow({ signal, targetLevel }) {
  const isMet = targetLevel === 1 ? signal.met_l1 : signal.met_l2;
  
  return (
    <div className="flex items-center justify-between py-2 px-3 rounded bg-slate-50">
      <div className="flex items-center gap-2">
        {isMet ? (
          <CheckCircle size={16} className="text-emerald-600" />
        ) : (
          <MinusCircle size={16} className="text-slate-400" />
        )}
        <span className="text-sm text-slate-700">{signal.label}</span>
      </div>
      <span className="text-sm font-medium text-slate-900">
        {formatValue(signal.value)}
      </span>
    </div>
  );
}

// Helper
function formatValue(val) {
  if (typeof val === 'boolean') return val ? 'Yes' : 'No';
  if (val < 1) return `${(val * 100).toFixed(0)}%`;
  return val.toFixed(1);
}
