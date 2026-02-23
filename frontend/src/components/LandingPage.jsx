import React from 'react';
import { motion } from 'framer-motion';
import { Sparkles, ArrowRight, BrainCircuit } from 'lucide-react';

const LandingPage = ({ onEnter }) => {
    return (
        <div className="min-h-screen flex flex-col items-center justify-center p-6 relative overflow-hidden">
            {/* Decorative background blobs */}
            <div className="absolute top-[-10%] left-[-10%] w-[40rem] h-[40rem] bg-pastel-pink/30 rounded-full blur-[100px] pointer-events-none" />
            <div className="absolute bottom-[-10%] right-[-10%] w-[40rem] h-[40rem] bg-pastel-purple/20 rounded-full blur-[100px] pointer-events-none" />

            <motion.div
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, ease: "easeOut" }}
                className="text-center z-10 max-w-2xl mx-auto"
            >
                <div className="flex justify-center mb-6">
                    <motion.div
                        initial={{ scale: 0.8, rotate: -15 }}
                        animate={{ scale: 1, rotate: 0 }}
                        transition={{ delay: 0.3, type: "spring", stiffness: 200 }}
                        className="p-4 bg-white rounded-2xl shadow-soft"
                    >
                        <BrainCircuit size={48} className="text-pastel-deep" />
                    </motion.div>
                </div>

                <h1 className="text-6xl md:text-7xl font-extrabold mb-6 tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-pastel-deep to-pink-400">
                    Retrievia
                </h1>

                <p className="text-xl text-pastel-gray mb-10 leading-relaxed max-w-lg mx-auto">
                    Your intelligent, conversational AI knowledge base. Effortlessly interact with your complex documents in a beautiful, unified workspace.
                </p>

                <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={onEnter}
                    className="group relative inline-flex items-center justify-center gap-2 bg-pastel-deep text-white px-8 py-4 rounded-full font-semibold text-lg hover:bg-pastel-dark transition-colors shadow-lg shadow-pastel-deep/30"
                >
                    <Sparkles size={20} className="animate-pulse" />
                    <span>Enter Chatbot</span>
                    <ArrowRight size={20} className="group-hover:translate-x-1 transition-transform" />
                </motion.button>
            </motion.div>
        </div>
    );
};

export default LandingPage;
