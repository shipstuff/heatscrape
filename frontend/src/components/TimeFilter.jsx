import './TimeFilter.css'

const TIME_OPTIONS = [
  { value: 'all', label: 'All Time' },
  { value: 'week', label: 'This Week' },
  { value: 'day', label: 'Today' },
]

function TimeFilter({ value, onChange }) {
  return (
    <div className="time-filter">
      {TIME_OPTIONS.map((option) => (
        <button
          key={option.value}
          className={`time-filter-btn ${value === option.value ? 'active' : ''}`}
          onClick={() => onChange(option.value)}
        >
          {option.label}
        </button>
      ))}
    </div>
  )
}

export default TimeFilter
