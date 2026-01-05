"use client";

import React, { useEffect, useRef, useState } from "react";
import { Mic, MicOff, Video, VideoOff, PhoneOff } from "lucide-react";

interface VideoCallProps {
  onStreamReady: (stream: MediaStream) => void;
  remoteStream: MediaStream | null; // NEW: Accept remote stream
  isAnalyzing: boolean;
  role?: "interviewer" | "candidate";
}

export default function VideoCall({
  onStreamReady,
  remoteStream,
  isAnalyzing,
  role = "interviewer",
}: VideoCallProps) {
  const localVideoRef = useRef<HTMLVideoElement>(null);
  const remoteVideoRef = useRef<HTMLVideoElement>(null);
  const [isMicOn, setIsMicOn] = useState(true);
  const [isCameraOn, setIsCameraOn] = useState(true);
  const [stream, setStream] = useState<MediaStream | null>(null);

  useEffect(() => {
    const startCamera = async () => {
      try {
        const mediaStream = await navigator.mediaDevices.getUserMedia({
          video: true,
          audio: true,
        });
        setStream(mediaStream);
        if (localVideoRef.current) {
          localVideoRef.current.srcObject = mediaStream;
        }
        onStreamReady(mediaStream);
      } catch (err) {
        console.error("Error accessing camera:", err);
      }
    };

    startCamera();

    return () => {
      if (stream) {
        stream.getTracks().forEach((track) => track.stop());
      }
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []); // Run once on mount

  // Handle Remote Stream Updates
  useEffect(() => {
    if (remoteVideoRef.current && remoteStream) {
      remoteVideoRef.current.srcObject = remoteStream;
    }
  }, [remoteStream]);

  const toggleMic = () => {
    if (stream) {
      const audioTrack = stream.getAudioTracks()[0];
      audioTrack.enabled = !audioTrack.enabled;
      setIsMicOn(audioTrack.enabled);
    }
  };

  const toggleCamera = () => {
    if (stream) {
      const videoTrack = stream.getVideoTracks()[0];
      videoTrack.enabled = !videoTrack.enabled;
      setIsCameraOn(videoTrack.enabled);
    }
  };

  return (
    <div className="relative w-full h-full bg-slate-900 rounded-2xl overflow-hidden shadow-2xl border border-slate-700">
      {/* REMOTE VIDEO (Main View) */}
      <div className="absolute inset-0 flex items-center justify-center bg-slate-800">
        {remoteStream ? (
          <video
            ref={remoteVideoRef}
            autoPlay
            playsInline
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="flex flex-col items-center">
            <div className="w-16 h-16 rounded-full border-4 border-slate-600 border-t-indigo-500 animate-spin mb-4" />
            <p className="text-slate-400 font-medium">
              {role === "interviewer"
                ? "Waiting for candidate to join..."
                : "Connecting to interviewer..."}
            </p>
          </div>
        )}
      </div>

      {/* LOCAL USER VIDEO (Picture-in-Picture) */}
      <div className="absolute bottom-4 right-4 w-48 h-36 bg-black rounded-xl overflow-hidden border-2 border-slate-600 shadow-lg z-10 transition-all hover:scale-105">
        <video
          ref={localVideoRef}
          autoPlay
          playsInline
          muted
          className={`w-full h-full object-cover transform scale-x-[-1] ${
            !isCameraOn ? "hidden" : ""
          }`}
        />
        {!isCameraOn && (
          <div className="absolute inset-0 flex items-center justify-center bg-slate-700">
            <VideoOff className="w-8 h-8 text-slate-400" />
          </div>
        )}
        <div className="absolute bottom-2 left-2 text-xs text-white bg-black/50 px-2 py-0.5 rounded">
          You ({role})
        </div>
      </div>

      {/* Main Overlay Gradient */}
      <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent pointer-events-none" />

      {/* Controls */}
      <div className="absolute bottom-6 left-1/2 transform -translate-x-1/2 flex items-center gap-4 z-20">
        <button
          onClick={toggleMic}
          className={`p-4 rounded-full transition-all ${
            isMicOn
              ? "bg-slate-700 hover:bg-slate-600 text-white"
              : "bg-red-500 hover:bg-red-600 text-white"
          }`}
        >
          {isMicOn ? <Mic size={24} /> : <MicOff size={24} />}
        </button>

        <button
          onClick={toggleCamera}
          className={`p-4 rounded-full transition-all ${
            isCameraOn
              ? "bg-slate-700 hover:bg-slate-600 text-white"
              : "bg-red-500 hover:bg-red-600 text-white"
          }`}
        >
          {isCameraOn ? <Video size={24} /> : <VideoOff size={24} />}
        </button>

        <button className="p-4 rounded-full bg-red-600 hover:bg-red-700 text-white transition-all shadow-lg hover:shadow-red-500/30">
          <PhoneOff size={24} />
        </button>
      </div>

      {/* Status Indicators */}
      <div className="absolute top-4 left-4 flex gap-2">
        {isAnalyzing && (
          <div className="flex items-center gap-2 px-3 py-1.5 bg-red-500/20 border border-red-500/50 rounded-full backdrop-blur-sm z-30">
            <div className="w-2 h-2 rounded-full bg-red-500 animate-pulse" />
            <span className="text-xs font-medium text-red-200">
              Live Analysis Active
            </span>
          </div>
        )}
      </div>
    </div>
  );
}
