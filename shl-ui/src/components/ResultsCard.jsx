export default function ResultsCard({ item }) {
    return (
      <div className="glass p-5 rounded-xl border-l-4 border-blue-600">
        <h3 className="text-lg font-semibold text-gray-900">{item.name}</h3>
        <a
          href={item.url}
          target="_blank"
          rel="noreferrer"
          className="text-blue-600 underline text-sm"
        >
          View Assessment →
        </a>
      </div>
    );
  }
  