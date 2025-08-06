import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import type { RecommendationResponse } from '../types';

interface Props {
  data: RecommendationResponse;
}

const RecommendationDisplay: React.FC<Props> = ({ data }) => {
  return (
    <div className="bg-gray-800/50 border border-gray-700 rounded-lg p-6 animate-fade-in">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          h1: ({node, ...props}) => <h1 className="text-3xl font-bold text-cyan-400 mb-4 border-b border-gray-600 pb-2" {...props} />,
          h2: ({node, ...props}) => <h2 className="text-2xl font-semibold text-cyan-300 mt-6 mb-3" {...props} />,
          h3: ({node, ...props}) => <h3 className="text-xl font-semibold mt-4 mb-2 text-gray-200" {...props} />,
          p: ({node, ...props}) => <p className="text-gray-300 leading-relaxed mb-4" {...props} />,
          ul: ({node, ...props}) => <ul className="list-disc list-inside space-y-2 mb-4 pl-4" {...props} />,
          li: ({node, ...props}) => <li className="text-gray-300" {...props} />,
          strong: ({node, ...props}) => <strong className="font-bold text-white" {...props} />,
          a: ({node, ...props}) => <a className="text-cyan-400 hover:text-cyan-300 underline transition" target="_blank" rel="noopener noreferrer" {...props} />,
          blockquote: ({node, ...props}) => <blockquote className="border-l-4 border-cyan-600 pl-4 text-gray-400 italic my-4" {...props} />,
        }}
      >
        {data.recommendation}
      </ReactMarkdown>
    </div>
  );
};


const styles = `
@keyframes fade-in {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in {
  animation: fade-in 0.5s ease-out forwards;
}
`;

// Bu stili dinamik olarak ekle
const styleSheet = document.createElement("style");
styleSheet.innerText = styles;
document.head.appendChild(styleSheet);


export default RecommendationDisplay;