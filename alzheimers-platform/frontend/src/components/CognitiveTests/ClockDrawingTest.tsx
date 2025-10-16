// frontend/src/components/CognitiveTests/ClockDrawingTest.tsx
import React, { useRef, useEffect } from 'react';
import { useFormContext } from 'react-hook-form';

interface Point {
  x: number;
  y: number;
}

const ClockDrawingTest: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const { setValue } = useFormContext();
  const [isDrawing, setIsDrawing] = React.useState(false);
  const [points, setPoints] = React.useState<Point[]>([]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Initialize canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 2;

    // Draw clock circle
    ctx.beginPath();
    ctx.arc(canvas.width / 2, canvas.height / 2, 150, 0, 2 * Math.PI);
    ctx.stroke();
  }, []);

  const handleMouseDown = (e: React.MouseEvent) => {
    setIsDrawing(true);
    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    setPoints([{ x, y }]);
  };

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!isDrawing) return;

    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    setPoints(prev => [...prev, { x, y }]);

    // Draw on canvas
    if (points.length > 0) {
      ctx.beginPath();
      ctx.moveTo(points[points.length - 1].x, points[points.length - 1].y);
      ctx.lineTo(x, y);
      ctx.stroke();
    }
  };

  const handleMouseUp = () => {
    setIsDrawing(false);
    // Save drawing to form data
    if (canvasRef.current) {
      setValue('clockDrawing', canvasRef.current.toDataURL());
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h3 className="text-xl font-semibold mb-4">Clock Drawing Test</h3>
      <p className="mb-4">Please draw a clock showing the time as "10 past 11"</p>

      <canvas
        ref={canvasRef}
        width={400}
        height={400}
        className="border border-gray-300 rounded-md"
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
      />

      <div className="mt-4 flex space-x-2">
        <button
          type="button"
          onClick={() => {
            const canvas = canvasRef.current;
            if (canvas) {
              const ctx = canvas.getContext('2d');
              if (ctx) {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                // Redraw clock circle
                ctx.beginPath();
                ctx.arc(canvas.width / 2, canvas.height / 2, 150, 0, 2 * Math.PI);
                ctx.stroke();
              }
            }
          }}
          className="px-4 py-2 bg-gray-200 rounded-md"
        >
          Clear
        </button>
      </div>
    </div>
  );
};

export default ClockDrawingTest;