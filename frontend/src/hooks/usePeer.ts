import { useEffect, useState, useRef, useCallback } from "react";
import Peer, { MediaConnection, DataConnection } from "peerjs";

export interface PeerState {
  myId: string;
  peer: Peer | null;
  remoteStream: MediaStream | null;
  isCallConnected: boolean;
  conn: DataConnection | null;
}

export function usePeer() {
  const [state, setState] = useState<PeerState>({
    myId: "",
    peer: null,
    remoteStream: null,
    isCallConnected: false,
    conn: null,
  });

  const peerRef = useRef<Peer | null>(null);
  const localStreamRef = useRef<MediaStream | null>(null);

  const setLocalStream = useCallback((stream: MediaStream) => {
    localStreamRef.current = stream;
  }, []);

  useEffect(() => {
    // Initialize Peer (auto-generate ID)
    const initPeer = async () => {
      // Dynamic import to avoid SSR issues with Next.js
      const { default: Peer } = await import("peerjs");
      const peer = new Peer();

      peer.on("open", (id) => {
        console.log("My Peer ID is: " + id);
        setState((prev) => ({ ...prev, myId: id, peer }));
        peerRef.current = peer;
      });

      // Handle incoming calls (Guest calling Host)
      peer.on("call", (call: MediaConnection) => {
        console.log("Receiving call from:", call.peer);
        if (localStreamRef.current) {
          console.log("Answering call with local stream");
          call.answer(localStreamRef.current);
          handleCall(call);
        } else {
          console.warn("No local stream available to answer call");
          // Optionally try to get it, or wait?
          // For now, we rely on setLocalStream being called before this event
          navigator.mediaDevices
            .getUserMedia({ video: true, audio: true })
            .then((stream) => {
              call.answer(stream);
              handleCall(call);
            })
            .catch((e) => console.error("Failed to get stream to answer", e));
        }
      });

      // Handle incoming data connections
      peer.on("connection", (conn: DataConnection) => {
        console.log("Data connection received");
        handleDataConnection(conn);
      });

      peer.on("error", (err) => {
        console.error("PeerJS Error:", err);
      });
    };

    initPeer();

    return () => {
      peerRef.current?.destroy();
    };
  }, []); // Remove dependency on localStreamRef.current to avoid re-init

  const handleCall = (call: MediaConnection) => {
    call.on("stream", (remoteStream) => {
      console.log("Received remote stream");
      setState((prev) => ({ ...prev, remoteStream, isCallConnected: true }));
    });
    call.on("close", () => {
      setState((prev) => ({
        ...prev,
        remoteStream: null,
        isCallConnected: false,
      }));
    });
    call.on("error", (e) => console.error("Call error", e));
  };

  const handleDataConnection = (conn: DataConnection) => {
    conn.on("open", () => {
      console.log("Data connection open");
      setState((prev) => ({ ...prev, conn }));
    });
    conn.on("data", (data) => {
      console.log("Received data:", data);
    });
    conn.on("error", (e) => console.error("Conn error", e));
  };

  const performCall = useCallback(
    (remoteId: string, localStream: MediaStream) => {
      if (!peerRef.current) {
        console.warn("Peer not ready to perform call");
        return;
      }
      localStreamRef.current = localStream;

      console.log("Calling peer:", remoteId);
      // Call remote peer
      const call = peerRef.current.call(remoteId, localStream);
      handleCall(call);

      // Connect data channel
      const conn = peerRef.current.connect(remoteId);
      handleDataConnection(conn);
    },
    []
  );

  const sendData = useCallback(
    (data: any) => {
      if (state.conn) {
        state.conn.send(data);
      }
    },
    [state.conn]
  );

  return {
    ...state,
    performCall,
    sendData,
    setLocalStream,
  };
}
