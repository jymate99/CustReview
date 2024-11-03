import { useState } from "react"
import { Button } from "../../@/components/ui/button"
import { Input } from "../../@/components/ui/input"
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "../../@/components/ui/card"

export function SentimentForm() {
  const [text, setText] = useState("")
  const [sentiment, setSentiment] = useState<number | null>(null)
  const [loading, setLoading] = useState(false)

  const analyzeSentiment = async () => {
    try {
      setLoading(true)
       //const response = await fetch(  "/api/predict"
       const response = await fetch(  "http://127.0.0.1:8000/predict"
        , {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text }),
      })
      console.log(({ text }))
      const data = await response.json()
      setSentiment(data.sentiment)
    } catch (error) {
      console.error("Error analyzing sentiment:", error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <Card className="w-[900px] bg-slate-800 border-2 border-blue-500 shadow-lg shadow-blue-500/20">
      <CardHeader>
        <CardTitle className="text-slate-100">Customer Review Cause Analysis</CardTitle>
        <CardDescription className="text-slate-300">
          Enter a customer review to analyze its root cause
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-8">
        <div className="flex space-x-4">
          <Input
            placeholder="Enter your review here..."
            value={text}
            onChange={(e) => setText(e.target.value)}
            className="bg-slate-700 text-slate-100 border-slate-600 focus:border-blue-500 placeholder:text-slate-400"
          />
          <Button 
            onClick={analyzeSentiment} 
            disabled={loading}
            className="bg-blue-500 hover:bg-blue-600 text-white"
          >
            {loading ? "Analyzing..." : "Analyze"}
          </Button>
        </div>
        {sentiment !== null && (
          <div className="text-center p-8 bg-slate-700 rounded-md border border-blue-500/50">
            <p className="font-semibold text-slate-100">Bad Review Reason: {sentiment}</p>
          </div>
        )}
      </CardContent>
    </Card>
  )
} 