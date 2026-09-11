%=========================================================================%
% config.m                                                                %
% Prettyplot 1.1, 01.06.2006                                              %
%                                                                         %
% Konfiguration von Prettyplot                                            %
%=========================================================================%
% globale Variablen
%--------------------------------------------------------------------------
global nn nf name count workingdir prettypath texexepath distillerpath ...
       gspath ratio xlimdiff ylimdiff surfplot
%--------------------------------------------------------------------------
% Zielformat (eps, pdf, png, jpg, tif), Dateizusatz, 
% Ausgabeort und -auflösung festlegen 
%--------------------------------------------------------------------------
outputformat='pdf';  
outputdirectory='.';
fileextension='';
outres=600;
%--------------------------------------------------------------------------
% Defaulteinstellungen für Linien, Balken, Marker, Formen usw.
%--------------------------------------------------------------------------
defaultlinestyle='-';
defaultlinewidth=1;
defaultlinecolor='b';
defaultlinemarker='none';
defaultbarcolor='b';
defaultbarwidth=0.1;
defaultmarkercolor='b';
defaultmarkerwidth=1;
defaultmarkerstyle='o';
defaultformcolor='y';
default3dview=[50,30];
%--------------------------------------------------------------------------
% Defaulteinstellungen für Schriftart, -größe, -ersetzungen usw.
%--------------------------------------------------------------------------
axisfontsize=12;
axisfontname='palatino'; 
psfragfont='palatino'; 
psfraggroesse=12;
psfragscale='normalsize';
allpsfrags=1;
%--------------------------------------------------------------------------
% max. Textbreite in cm
%--------------------------------------------------------------------------
textbreite=17.7;  
%--------------------------------------------------------------------------
% Einstellungen für LaTeX
%--------------------------------------------------------------------------
texincludes={'./../../Titel/packages.tex' './../../Titel/befehle.tex'};
texauxfile='./../../bericht.aux';
%--------------------------------------------------------------------------
% Graustufen?
%--------------------------------------------------------------------------
grayscaleplot=0; 
%--------------------------------------------------------------------------
% Defaulteinstellungen
%--------------------------------------------------------------------------
farbe_k=[0 0 0];
farbe_b=[0.0 0.0 1.0];
farbe_r=[1.0 0.0 0.0];
farbe_g=[0.2 0.6 0.4];
farbe_y=[1.0 1.0 0.0];
farbe_c=[0.0 1.0 1.0];
farbe_m=[1.0 0.0 1.0];
farbe_w=[1.0 1.0 1.0];
farbe_h=[0.4 0.7 0.9];
%--------------------------------------------------------------------------
% Defaulteinstellungen überschreiben
%--------------------------------------------------------------------------
if grayscaleplot==1 
   colormap('gray');
   farbe_k=[0 0 0];
   farbe_b=[0.0 0.0 0.0];
   farbe_r=[0.2 0.2 0.2];
   farbe_g=[0.5 0.5 0.5];
   farbe_y=[0.8 0.8 0.8];
   farbe_c=[0.4 0.4 0.4];
   farbe_m=[0.6 0.6 0.6];
   farbe_w=[1.0 1.0 1.0];
end
%--------------------------------------------------------------------------
% Daten für Dummyplot (Hilfe bei Erstellung von Legenden)
%--------------------------------------------------------------------------
dummyx=[1e30:1e30];
dummyy=[1e30:1e30];
%--------------------------------------------------------------------------
% Zuordnungsmatrix (nicht ändern!)
%--------------------------------------------------------------------------
if outputformat=='eps'
   mat=[1 1 1 0 0 0; ...
        1 1 0 0 0 0; ...
        0 0 1 0 0 0; ...
        1 0 0 0 0 0; ...
        0 1 1 0 0 0; ...
        0 0 1 0 0 0; ...
        0 0 0 0 0 1;...
        0 0 0 0 1 0];
elseif outputformat=='pdf'
   mat=[1 1 1 1 0 0; ...
        1 1 0 0 0 0; ...
        0 0 1 1 0 0; ...
        1 0 0 0 0 0; ...
        0 1 1 1 0 0; ...
        0 0 1 0 0 0; ...
        0 0 0 0 0 1;...
        0 0 0 0 1 0];
else
   mat=[1 1 1 0 1 0; ...
        1 1 0 0 1 0; ...
        0 0 1 0 1 0; ...
        1 0 0 0 1 0; ...
        0 1 1 0 1 0; ...
        0 0 1 0 1 0; ...
        0 0 0 0 0 1;...
        0 0 0 0 1 0];    
end    
%--------------------------------------------------------------------------
% Dateiende
%--------------------------------------------------------------------------
