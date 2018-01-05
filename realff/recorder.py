import matplotlib
matplotlib.use('TkAgg') # <-- THIS MAKES IT FAST!
import numpy
import scipy
import struct
import pyaudio
import threading
import pylab
import struct
import sys

#this can be used for fast calucations i.e. for time period 0.1,0.2 seconds
class Recorder:
    """Simple, cross-platform class to record from the microphone."""
    
    def __init__(self):
        """minimal garb is executed when class is loaded."""
        self.RATE=44100
        self.BUFFERSIZE=int(float(sys.argv[1])*40960)
        self.secToRecord=float(sys.argv[1])
        self.threadsDieNow=False
        self.newAudio=False
        
    def setup(self):
        """initialize sound card."""
        #TODO - windows detection vs. alsa or something for linux---there is always error in alsa
        #TODO - try/except for sound card selection/initiation

        self.buffersToRecord=int(self.RATE*self.secToRecord/self.BUFFERSIZE)
        if self.buffersToRecord==0: self.buffersToRecord=1
        self.samplesToRecord=int(self.BUFFERSIZE*self.buffersToRecord)
        self.chunksToRecord=int(self.samplesToRecord/self.BUFFERSIZE)
        self.secPerPoint=1.0/self.RATE
        
        self.p = pyaudio.PyAudio()
        self.inStream = self.p.open(format=pyaudio.paInt16,channels=1,rate=self.RATE,input=True,frames_per_buffer=self.BUFFERSIZE)#16 bit int
        
        self.xsBuffer=numpy.arange(self.BUFFERSIZE)*self.secPerPoint##creating array[0 1 2 ...1024]
        self.xs=numpy.arange(self.chunksToRecord*self.BUFFERSIZE)*self.secPerPoint###if secToRecord=0.5 dividing into 1/rate
        #self.ts=numpy.arange(self.secToRecord*self.BUFFERSIZE)
        self.audio=numpy.empty((self.chunksToRecord*self.BUFFERSIZE),dtype=numpy.int16)  ##crucial             
    
    def close(self):
        """cleanly back out and release sound card."""
        self.p.close(self.inStream)
    
    ### RECORDING AUDIO ###  
    
    def getAudio(self):
        """get a single buffer size worth of audio."""
        audioString=self.inStream.read(self.BUFFERSIZE)
        return numpy.fromstring(audioString,dtype=numpy.int16)
        
    def record(self,forever=True):
        """record secToRecord seconds of audio."""
        while True:
            if self.threadsDieNow: break
            for i in range(self.chunksToRecord):
                self.audio[i*self.BUFFERSIZE:(i+1)*self.BUFFERSIZE]=self.getAudio()
            self.newAudio=True 
            if forever==False: break
    
    def continuousStart(self):
        """CALL THIS to start running forever."""
        self.t = threading.Thread(target=self.record)########
        self.t.start()
        
    def continuousEnd(self):
        """shut down continuous recording."""#############
        self.threadsDieNow=True

    ### MATH ###
        
    def fft(self,data=None,trimBy=5,calibr=1.1,divBy=400):
        if data==None: 
            data=self.audio.flatten()
        left,right=numpy.split(numpy.abs(numpy.fft.fft(data)),2)
        ys=numpy.add(left,right[::-1])
        ys=numpy.multiply(20,numpy.log10(ys))### depending upon standards ..
        xs=numpy.arange(self.BUFFERSIZE/self.secToRecord,dtype=float)
        if trimBy:
            i=int((self.BUFFERSIZE)/trimBy)##### change the length of i to increase the x axis ---much noise...
            ys=ys[50:i]
            xs=xs[50:i]*self.RATE/self.BUFFERSIZE
        if divBy:
            ys=ys/float(divBy)
            print xs
            ps=numpy.sum(ys)**0.5
            ps=ps/float(calibr)
            print("dB:",ps)
        return xs,ys
    
    ### VISUALIZATION ###
    
    def plotAudio(self):
        """open a matplotlib popup window showing audio data."""
        pylab.plot(self.audio.flatten())
        pylab.show()        
            
