%---------------------------------------------------------------
% Dokumentenklasse für Dissertationen sowie
% Studien-, Projekt- und Diplomarbeiten am IAT
%---------------------------------------------------------------
% Vision 3.3, 2021 von Bsher Karbouj, TU Berlin.
%--------------------------------------------------------------

%---------------------------------------------------------------
\NeedsTeXFormat{LaTeX2e}
%----------------------------------------------------------------
\ProvidesClass{Styles/Dokument/iat}
  
%----------------------------------------------------------------
\newif\if@restonecol
\newif\if@openright
\newif\if@draft
\newif\ifdissvorgelegt
\newif\ifdissgenehmigt
\newif\ifdissreferenten
\newif\ifindividuell
\newif\ifba
\newif\ifda
\newif\ifpa
\newif\ifma
\newif\ifla
\newif\ifdatitelseite
\newif\ifnotitlefigure
\newif\ifbericht
\newif\ifusenglish
\newif\ifngerman
\newif\ifabschluss

%----------------------------------------------------------------
% Optionen deklarieren
%----------------------------------------------------------------
% einseitig (Standard) für DA, zweiseitig für Diss
\DeclareOption{oneside}{\@twosidefalse \@mparswitchfalse}
\DeclareOption{twoside}{\@twosidetrue  \@mparswitchtrue}

% openright fängt Kapitel immer auf rechter Seite an.
\DeclareOption{openright}{\@openrighttrue}
\DeclareOption{openany}{\@openrightfalse}

% twocolumn ist prinzipiell möglich, aber nicht sinnvoll
%\DeclareOption{onecolumn}{\@twocolumnfalse}
%\DeclareOption{twocolumn}{\@twocolumntrue}

% Bilder nicht suchen sondern einheitlich durch Box ersetzen
\DeclareOption{draft}{\@drafttrue}
\DeclareOption{final}{\@draftfalse}

% Optionen zur Gestaltung der Titelseite
\DeclareOption{la}{\datitelseitetrue\latrue\dissvorgelegtfalse\dissgenehmigtfalse}
\DeclareOption{da}{\datitelseitetrue\datrue\dissvorgelegtfalse\dissgenehmigtfalse\abschlusstrue}
\DeclareOption{ma}{\datitelseitetrue\matrue\dissvorgelegtfalse\dissgenehmigtfalse\abschlusstrue}
\DeclareOption{ba}{\datitelseitetrue\batrue\dissvorgelegtfalse\dissgenehmigtfalse\abschlusstrue}
\DeclareOption{pa}{\datitelseitetrue\patrue\dissvorgelegtfalse\dissgenehmigtfalse}
\DeclareOption{bericht}{\berichttrue\dissvorgelegtfalse\dissgenehmigtfalse}
\DeclareOption{dissvorgelegt}{\dissvorgelegttrue\dissgenehmigtfalse}
\DeclareOption{dissgenehmigt}{\dissgenehmigttrue\dissvorgelegtfalse}
\DeclareOption{dissreferenten}{\dissreferententrue}
\DeclareOption{notitlefigure}{\notitlefiguretrue}
\DeclareOption{individuell}{\individuelltrue\dissvorgelegtfalse\dissgenehmigtfalse}

% Optionen zur Sprachauswahl
\DeclareOption{usenglish}{\usenglishtrue\ngermanfalse}
\DeclareOption{ngerman}{\ngermantrue\usenglishfalse}

% Formeln linksbündig setzen
\DeclareOption{fleqn}{\input{fleqn.clo}}
\DeclareOption{ceqn}{}

\ExecuteOptions{oneside,openany,final,dissvorgelegt,ceqn,usenglish}
\ProcessOptions
%----------------------------------------------------------------
% Schriftgrößen definieren
%----------------------------------------------------------------
% Standard: 12 Punkt (16 oder 18 Punkt Zeilenabstand)
\renewcommand\normalsize{%
   \@setfontsize\normalsize\@xiipt{16}%
%   \@setfontsize\normalsize\@xiipt{18}%
   \abovedisplayskip 8\p@ \@plus3\p@
   \belowdisplayskip \abovedisplayskip
   \abovedisplayshortskip \z@ \@plus3\p@
   \belowdisplayshortskip \abovedisplayskip
   \let\@listi\@listI}
\normalsize
% Small: 11 Punkt (14 oder 16 Punkt Abstand)
\newcommand\small{%
   \@setfontsize\small\@xipt{14}%
%   \@setfontsize\small\@xipt{16}%
   \abovedisplayskip 6\p@ \@plus2\p@
   \belowdisplayskip \abovedisplayskip
   \abovedisplayshortskip \z@ \@plus2\p@
   \belowdisplayshortskip \abovedisplayskip
   \def\@listi{\leftmargin\leftmargini
               \topsep 9\p@ \@plus3\p@ \@minus5\p@
               \parsep 4.5\p@ \@plus2\p@ \@minus\p@
               \itemsep \parsep}%
}
\newcommand\footnotesize{%
   \@setfontsize\footnotesize\@xpt\@xiipt
   \abovedisplayskip 4\p@ \@plus1\p@
   \belowdisplayskip \abovedisplayskip
   \abovedisplayshortskip \z@ \@plus1\p@
   \belowdisplayshortskip \abovedisplayskip
   \def\@listi{\leftmargin\leftmargini
               \topsep 6\p@ \@plus2\p@ \@minus2\p@
               \parsep 3\p@ \@plus2\p@ \@minus\p@
               \itemsep \parsep}%
}
\newcommand\scriptsize{\@setfontsize\scriptsize\@viiipt{9.5}}
\newcommand\tiny{\@setfontsize\tiny\@vipt\@viipt}
\newcommand\large{\@setfontsize\large\@xivpt{18}}
\newcommand\Large{\@setfontsize\Large\@xviipt{22}}
\newcommand\LARGE{\@setfontsize\LARGE\@xxpt{25}}
\newcommand\huge{\@setfontsize\huge\@xxvpt{30}}
\let\Huge=\huge
%----------------------------------------------------------------
% Skips
%----------------------------------------------------------------
\setlength\smallskipamount{3\p@ \@plus 1\p@ \@minus 1\p@}
\setlength\medskipamount{6\p@ \@plus 2\p@ \@minus 2\p@}
\setlength\bigskipamount{12\p@ \@plus 4\p@ \@minus 4\p@}
%----------------------------------------------------------------
% Kopf- und Fußzeilenabstände
%----------------------------------------------------------------
\setlength\headheight{12\p@}
\setlength\headsep   {24\p@}
\setlength\topskip   {12\p@}
\setlength\footskip  {36\p@}
\setlength\maxdepth  {.5\topskip}
%----------------------------------------------------------------
% Papiergröße
%----------------------------------------------------------------
\hoffset-1in
\voffset-1in
\setlength\paperheight {297mm}
\setlength\paperwidth  {210mm}
\setlength\overfullrule{0\p@}
%----------------------------------------------------------------
% Textbreite und -höhe
%----------------------------------------------------------------
\setlength\textwidth  {165mm}
\setlength\textheight {240mm}
%----------------------------------------------------------------
% Randkommentarbreite
%----------------------------------------------------------------
\setlength\marginparsep{3\p@}
\setlength\marginparpush{7\p@}
\setlength\marginparwidth{40\p@}
%----------------------------------------------------------------
% linke Seitenränder gerade und ungerade Seiten
%----------------------------------------------------------------
\setlength\oddsidemargin  {22mm}
\setlength\evensidemargin {22mm}
%----------------------------------------------------------------
% Oberer Seitenrand
%----------------------------------------------------------------
\setlength\topmargin {17mm}
%----------------------------------------------------------------
% Diverse Abstände
%----------------------------------------------------------------
\frenchspacing         % Nach Punkt kein größerer Abstand
\setlength{\unitlength}{1pt}
\setlength\footnotesep{8.4\p@}
\setlength{\skip\footins}{10.8\p@ \@plus 4\p@ \@minus 2\p@}   
\setlength\floatsep    {8\p@ \@plus 2\p@ \@minus 2\p@}        % Abstand zwischen Gleitobjekten
\setlength\textfloatsep{8\p@ \@plus 2\p@ \@minus 2\p@}        % Abstand zwischen Gleitobjekt[t,b] und Text
\setlength\intextsep   {8\p@ \@plus 2\p@ \@minus 2\p@}        % Abstand zwischen Gleitobjekt[h] und Text
\setlength\dblfloatsep    {8\p@ \@plus 2\p@ \@minus 2\p@}     % Abstand zwischen Gleitobjekten bei zweispaltigem Satz
\setlength\dbltextfloatsep{8\p@ \@plus 2\p@ \@minus 2\p@}     % Abstand zwischen Gleitobjekt[t,b] und Text zweispaltig
\setlength\@fptop{0\p@ \@plus 1fil}
\setlength\@fpsep{10\p@ \@plus 2fil}
\setlength\@fpbot{0\p@ \@plus 1fil}
\setlength\@dblfptop{0\p@ \@plus 1fil}
\setlength\@dblfpsep{10\p@ \@plus 2fil}
\setlength\@dblfpbot{0\p@ \@plus 1fil}
\setlength\partopsep{3\p@ \@plus 2\p@ \@minus 2\p@}
%----------------------------------------------------------------
% Listenabstände (Itemize etc.)
%----------------------------------------------------------------
\def\@listi{\leftmargin\leftmargini
%            \parsep 5\p@  \@plus2.5\p@ \@minus\p@
%            \topsep 10\p@ \@plus4\p@   \@minus6\p@
%            \itemsep5\p@  \@plus2.5\p@ \@minus\p@}
            \parsep \z@
            \topsep \z@
            \itemsep 6\p@}
\let\@listI\@listi
\@listi
\def\@listii {\leftmargin\leftmarginii
              \labelwidth\leftmarginii
              \advance\labelwidth-\labelsep
              \topsep    5\p@   \@plus2.5\p@ \@minus\p@
              \parsep    2.5\p@ \@plus\p@    \@minus\p@
              \itemsep   \parsep}
\def\@listiii{\leftmargin\leftmarginiii
              \labelwidth\leftmarginiii
              \advance\labelwidth-\labelsep
              \topsep    2.5\p@\@plus\p@\@minus\p@
              \parsep    \z@
              \partopsep \p@ \@plus\z@ \@minus\p@
              \itemsep   \topsep}
\def\@listiv {\leftmargin\leftmarginiv
              \labelwidth\leftmarginiv
              \advance\labelwidth-\labelsep}
\def\@listv  {\leftmargin\leftmarginv
              \labelwidth\leftmarginv
              \advance\labelwidth-\labelsep}
\def\@listvi {\leftmargin\leftmarginvi
              \labelwidth\leftmarginvi
              \advance\labelwidth-\labelsep}
%---------------------------------------------------------------
% Zeilenabstände
%---------------------------------------------------------------
\setlength\lineskip{0\p@}
\setlength\normallineskip{0\p@}
\renewcommand\baselinestretch{}
\setlength\parskip{8\p@ \@plus \p@}
\setlength\parindent{0\p@}
\@lowpenalty   51
\@medpenalty  151
\@highpenalty 301
%---------------------------------------------------------------
% Zähler für Float-Objekte
%---------------------------------------------------------------
\setcounter{topnumber}{1}
\renewcommand\topfraction{.7}
\setcounter{bottomnumber}{1}
\renewcommand\bottomfraction{.3}
\setcounter{totalnumber}{2}
\renewcommand\textfraction{.2}
\renewcommand\floatpagefraction{.5}
\setcounter{dbltopnumber}{2}
\renewcommand\dbltopfraction{.7}
\renewcommand\dblfloatpagefraction{.5}
%---------------------------------------------------------------
% Kopfzeilen
%---------------------------------------------------------------
\if@twoside
  \def\ps@headings{%
      \let\@oddfoot\@empty\let\@evenfoot\@empty
      \def\@evenhead{\thepage \hfil \slshape \leftmark}%
      \def\@oddhead{{\slshape\rightmark}\hfil{\thepage}}%
      \let\@mkboth\markboth
    \def\chaptermark##1{%
      \markboth {%
        \ifnum \c@secnumdepth >\m@ne
            \@chapapp\ \thechapter: \ %
        \fi
        ##1}{}}%
    \def\sectionmark##1{%
      \markright {%
        \ifnum \c@secnumdepth >\z@
          \thesection \ \ %
        \fi
        ##1}}}
\else
  \def\ps@headings{%
    \let\@oddfoot\@empty
    \def\@oddhead{{\slshape\rightmark}\hfil\thepage}%
    \let\@mkboth\markboth
    \def\chaptermark##1{%
      \markright {%
        \ifnum \c@secnumdepth >\m@ne
            \@chapapp\ \thechapter: \ %
        \fi
        ##1}}}
\fi
%---------------------------------------------------------------
% Defaultseitenlayout und Kopfzeilen
%---------------------------------------------------------------
\def\ps@kapitelbeginn{%      
      \let\@oddfoot\@empty
      \let\@evenfoot\@empty
      \def\@evenhead{\thepage}%
      \def\@oddhead{\hfil\thepage}
      }
\def\ps@mypagestyle{%
      \let\@oddfoot\@empty
      \let\@evenfoot\@empty
      \def\@evenhead{\thepage}%
      \def\@oddhead{\hfil\thepage}}
\def\ps@kapitelsolo{%
      \let\@oddfoot\@empty
      \let\@evenfoot\@empty
      \def\@evenhead{\thepage}%
      \def\@oddhead{\hfil\thepage}}
\if@twoside
  \def\ps@firsthead{%
      \let\@oddfoot\@empty
      \let\@evenfoot\@empty
      \def\@evenhead{\thepage}%
      \def\@oddhead{\hfil\thepage}}
\else
  \def\ps@firsthead{%
    \let\@oddfoot\@empty
    \def\@oddhead{\hfil\thepage}}
\fi
%---------------------------------------------------------------
% Titelseite
%---------------------------------------------------------------
\newcommand{\maketitle}{
\pagenumbering{Roman}
\ifx\iattitel\undefined\newcommand{\iattitel}{}\fi
\ifx\iatuntertitel\undefined\newcommand{\iatuntertitel}{}\fi
\ifx\iatverfasser\undefined\newcommand{\iatverfasser}{}\fi
\ifx\iatgebdatum\undefined\newcommand{\iatgebdatum}{}\fi
\ifx\iatgebort\undefined\newcommand{\iatgebort}{}\fi
\ifx\iatpromotionstag\undefined\newcommand{\iatpromotionstag}{}\fi
\ifx\iatpromotionsmonat\undefined\newcommand{\iatpromotionsmonat}{}\fi
\ifx\iatpromotionsjahr\undefined\newcommand{\iatpromotionsjahr}{}\fi
\ifx\iatinventarnr\undefined\newcommand{\iatinventarnr}{}\fi
\ifx\selectlanguage\undefined\else
\ifusenglish\selectlanguage{USenglish}\else\selectlanguage{ngerman}\fi
\fi
\begin{titlepage}
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% individuell
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
\ifindividuell
\input{Prolog/titelseite.tex}
\fi

\ifbericht
\vspace*{20mm} \begin{flushright} \includegraphics[scale=0.7]{Prolog/Logos/BAM-Logo-2015.png} \end{flushright}
\vspace*{-20mm} \begin{flushright} \includegraphics[scale=0.7]{Prolog/Logos/iat_logo.pdf} \end{flushright}
\vspace*{18mm}
\begin{center}
{\linespread{2}\selectfont {\large Institut für Werkzeugmaschinen und Fabrikbetrieb } \par}
{\linespread{1.5}\selectfont {\large Fachgebiet Industrielle Automatisierungstechnik} \par}
{\linespread{1.5}\selectfont {\large Prof. Dr.-Ing. Jörg Krüger } \par}
\vspace*{18mm}
{\linespread{2}\selectfont \textbf{\LARGE \iattitel} \par}
{\linespread{1.5}\selectfont \textbf{\large \iatuntertitel} \par}
\vfill
\vfill
\textbf{\iatverfasser} \\
\textbf{\iatpromotionsmonat}~\textbf{\iatpromotionsjahr}
\end{center}
\newpage
\fi


\ifdissgenehmigt
\begin{center}
\vspace*{2cm}
{\linespread{2}\selectfont \textbf{\Huge  \iattitel} \par}
\vfill
Von der Fakultät für Verkehrs- und Maschinensysteme \\
der Technischen Universität Berlin \\
zur Erlangung des akademischen Grades\\
Doktor-Ingenieur\\
genehmigte\par
\vspace{2cm}
\textbf{Dissertation}\par
\vspace{2cm}
von \\  \textbf{\iatverfasser} \\ geb. am \iatgebdatum~ in \iatgebort \\ \vspace{1cm} \textbf{\iatpromotionsjahr}
\end{center}
%\ifdissreferenten
\newpage
\thispagestyle{empty}
\vspace*{\fill}
1. Referent: \iatreferenteins\\ 
2. Referent: \iatreferentzwei\\ 
\ifx\iatreferentdrei\undefined
\else
3. Referent: \iatreferentdrei\\ \\
\fi
Tag der Promotion: \iatpromotionstag.~\iatpromotionsmonat~\iatpromotionsjahr
\newpage
%\fi
\fi

\ifdissvorgelegt
\begin{center}
\vspace*{2cm}
{\linespread{2}\selectfont \textbf{\Huge  \iattitel} \par}
\vfill
Der Fakultät für Verkehrs- und Maschinensysteme \\ derTechnischen Universität Berlin \\ zur Erlangung des akademischen Grades\\ Doktor-Ingenieur\\
vorgelegte\par
\vspace{2cm}
\textbf{Dissertation}\par
\vspace{2cm}
von \\  \textbf{\iatverfasser} \\ geb. am \iatgebdatum~ in \iatgebort \\ \vspace{1cm} \textbf{\iatpromotionsjahr}
\end{center}
\fi

\ifdatitelseite
\begin{flushleft}
\begin{minipage}{0.49\textwidth}
    \includegraphics[scale=0.06]{Prolog/Logos/BAM-Logo-2015.png}
\end{minipage}
\hfill
\begin{minipage}{0.49\textwidth}
    \begin{flushright}
        \includegraphics[scale=0.7]{Prolog/Logos/iat_logo.pdf}
    \end{flushright}
\end{minipage}
\end{flushleft}
\vspace*{18mm}
\begin{center}
{\linespread{2}\selectfont {\large Institute of Machine Tools and Factory Management } \par}
{\linespread{1.5}\selectfont {\large Department of Industrial Automation Technology} \par}
{\linespread{1.5}\selectfont {\large Prof. Dr.-Ing. Jörg Krüger } \par}
\vspace*{18mm}
{\linespread{2}\selectfont \textbf{\LARGE \iattitel} \par}
{\linespread{1.5}\selectfont {\large \iatuntertitel} \par}

\fi

\end{center}


\vspace*{15mm}

\begin{center}
\ifma \textbf{\Large Bachelor’s Thesis \iatinventarnr} \fi
\\[1.5cm]

\textbf{\iatverfasser} \\
\ifx\iatmatrikelnr\undefined\else Matrikelnummer: \iatmatrikelnr \\ \\[1.5cm]


\textbf{Primary Examiner:} \iatreferenteins \\
\textbf{Supervisor:} \iatreferentdrei \\
\textbf{External Supervisor:} \iatreferentzwei \\
\\[1.5cm]
\iatpromotionstag
\end{center}

\ifabschluss

\input{Prolog/erklaerung}
\fi
%\input{Prolog/aufgabenstellung}
%\fi
\end{titlepage}
\cleardoublepageempty
}
%
%---------------------------------------------------------------
% Kapitelnumerierung
%---------------------------------------------------------------
\newcommand*\chaptermark[1]{}
\setcounter{secnumdepth}{3}
\newcounter {part}
\newcounter {chapter}
\newcounter {section}[chapter]
\newcounter {subsection}[section]
\newcounter {subsubsection}[subsection]
\newcounter {paragraph}[subsubsection]
\newcounter {subparagraph}[paragraph]
\renewcommand \thepart {\@Roman\c@part}
\renewcommand \thechapter {\@arabic\c@chapter}
\renewcommand \thesection {\thechapter.\@arabic\c@section}
\renewcommand\thesubsection   {\thesection.\@arabic\c@subsection}
\renewcommand\thesubsubsection{\thesubsection .\@arabic\c@subsubsection}
\renewcommand\theparagraph    {\thesubsubsection.\@arabic\c@paragraph}
\renewcommand\thesubparagraph {\theparagraph.\@arabic\c@subparagraph}
%---------------------------------------------------------------
% Definition: Part
%---------------------------------------------------------------
\newcommand\@chapapp{\chaptername}
\newcommand\part{%
  \if@openright
    \cleardoublepage
  \else
    \clearpage
  \fi
%  \thispagestyle{firsthead}%
% geändert  !!!!!!!!!!!!

  \thispagestyle{empty}%
  \if@twocolumn
    \onecolumn
    \@tempswatrue
  \else
    \@tempswafalse
  \fi
  \null\vfil
  \secdef\@part\@spart}

\def\@part[#1]#2{%
    \ifnum \c@secnumdepth >-2\relax
      \refstepcounter{part}%
      \addcontentsline{toc}{part}{\thepart\hspace{1em}#1}%      
    \else
      \addcontentsline{toc}{part}{#1}%
    \fi
    \markboth{}{}%
    {\centering
     \interlinepenalty \@M
     \normalfont
     \ifnum \c@secnumdepth >-2\relax
       \huge\bfseries \partname~\thepart
       \par
       \vskip 20\p@
     \fi
     \Huge \bfseries #2\par}%
    \@endpart}
\def\@spart#1{%
    {\centering
     \interlinepenalty \@M
     \normalfont
     \Huge \bfseries #1\par}%
    \@endpart}
\def\@endpart{\vfil\newpage
              \if@twoside
               \if@openright
                \null
                \thispagestyle{empty}%
                \newpage
               \fi
              \fi
              \if@tempswa
                \twocolumn
              \fi}
%---------------------------------------------------------------
% Definition: Chapter
%---------------------------------------------------------------
% Größe von huge in LARGE geändert!!!

\newcommand\chapter{\if@openright
                      \cleardoublepageempty\thispagestyle{empty}
                    \else
                      \clearpage
                    \fi
%                    \thispagestyle{kapitelbeginn}
%                    \thispagestyle{firsthead}
%                    \thispagestyle{empty}
                    \global\@topnum\z@
                    \@afterindentfalse
                    \secdef\@chapter\@schapter}
\newcommand\chaptera{
                    \if@openright
                      \thispagestyle{empty}
                    \fi
                    \global\@topnum\z@
                    \@afterindentfalse
                    \secdef\@chapter\@schapter
                    }
                    
                    
\newcommand\chaptere{
\thispagestyle{empty}%
                    \global\@topnum\z@
                    \@afterindentfalse
                    \secdef\@chapter\@schapter}
                    

\def\@chapter[#1]#2{\ifnum \c@secnumdepth >\m@ne
                         \refstepcounter{chapter}%
                         \typeout{\@chapapp\space\thechapter.}%
                         \addcontentsline{toc}{chapter}%
                                   {\protect\numberline{\thechapter}#1}%
                    \else
                      \addcontentsline{toc}{chapter}{#1}%
                    \fi
                    \chaptermark{#1}%
                    \addtocontents{lof}{\protect\addvspace{10\p@}}%
                    \addtocontents{lot}{\protect\addvspace{10\p@}}%
                    \if@twocolumn
                      \@topnewpage[\@makechapterhead{#2}]%
                    \else
                      \@makechapterhead{#2}%
                      \@afterheading
                    \fi}
\def\@makechapterhead#1{%
  \vspace*{30\p@}%
  {\parindent \z@ \raggedright \normalfont
    \interlinepenalty\@M
    \LARGE \bfseries
    \ifnum \c@secnumdepth >\m@ne
% Lars: Änderung für vernünftige Einrückung mehrzeiliger Chapterüberschriften 
% neu (Pfuschlösung - Schriftgröße beachten!)
    \begin{tabular}[t]{@{}p{.062\textwidth} @{}p{.938\textwidth}} 
    \leftline{\thechapter} \hspace{19pt} & \raggedright {#1}
    \end{tabular}       
% alt:
%         \thechapter \hspace{14pt}
    \fi
%    #1\par\nobreak
    \vskip 40\p@
  }}
\def\@schapter#1{\if@twocolumn
                   \@topnewpage[\@makeschapterhead{#1}]%
                 \else
                   \@makeschapterhead{#1}%
                   \@afterheading
                 \fi}
\def\@makeschapterhead#1{%
  \vspace*{30\p@}%
  {\parindent \z@ \raggedright
    \normalfont
    \interlinepenalty\@M
    \LARGE \bfseries  #1
    \par \nobreak
    \vskip 40\p@
  }}
\newcommand\header[1]{
  \chapter*{#1}
  \if@openright
   \thispagestyle{empty}
  \fi
  \addcontentsline{toc}{chapter}{#1}
  \markboth{\headertextfont #1}{#1}
}
\newcommand\headers[1]{
  \chapter*{#1}
  \if@openright
   \thispagestyle{empty}
  \fi
  \markboth{\headertextfont #1}{#1}
}
\newcommand\headerempty[1]{
  \chapter*{#1}
  \markboth{}{}
}


\newcommand\newheader[1]{
  \newpage
  \thispagestyle{firsthead}
  \vspace*{39.1\p@}
  {\bf \LARGE #1}
  \vskip 40\p@
  \mtcaddchapter[#1]
  \markboth{#1}{#1}
}




%---------------------------------------------------------------
% Definition: Section
%---------------------------------------------------------------
%\renewcommand\chapter{\@startsection {chapter}{1}{\z@}% 
%                                   {-3.5ex \@plus -1ex \@minus -.2ex}%
%                                   {2.3ex \@plus.2ex}%
%                                   {\normalfont\LARGE\bfseries}}


%---------------------------------------------------------------
% Definition: Section
%---------------------------------------------------------------
\newcommand\section{\@startsection {section}{1}{\z@}% 
                                   {-3.5ex \@plus -1ex \@minus -.2ex}%
                                   {2.3ex \@plus.2ex}%
                                   {\normalfont\Large\bfseries}}
%---------------------------------------------------------------
% Definition: Subsection
%---------------------------------------------------------------
\newcommand\subsection{\@startsection{subsection}{2}{\z@}%
                                     {-3.25ex\@plus -1ex \@minus -.2ex}%
                                     {1.5ex \@plus .2ex}%
                                     {\normalfont\large\bfseries}}
%---------------------------------------------------------------
% Definition: Subsubsection
%---------------------------------------------------------------
\newcommand\subsubsection{\@startsection{subsubsection}{3}{\z@}%
                                     {-1ex \@plus -0.5ex}%
%                                     {-3.25ex\@plus -1ex \@minus -.2ex}%
                                     {0.1ex}%
%                                     {1.5ex \@plus .2ex}%
                                     {\normalfont\normalsize\bfseries}}
%---------------------------------------------------------------
% Definition: Paragraph
%---------------------------------------------------------------
\newcommand\paragraph{\@startsection{paragraph}{4}{\z@}%
                                    {1ex \@plus1ex \@minus.2ex}%
                                    {-0.5em}%
                                    {\normalfont\normalsize\bfseries}}
%---------------------------------------------------------------
% Definition: Subparagraph
%---------------------------------------------------------------
\newcommand\subparagraph{\@startsection{subparagraph}{5}{\parindent}%
                                       {0ex}
                                       {-0.5em}%
                                      {\normalfont\normalsize\bfseries}}
%---------------------------------------------------------------
% Seitenränder für Listen
%---------------------------------------------------------------
\if@twocolumn
  \setlength\leftmargini  {2em}
\else
  \setlength\leftmargini  {2.5em}
\fi
\leftmargin  \leftmargini
\setlength\leftmarginii  {2.2em}
\setlength\leftmarginiii {1.87em}
\setlength\leftmarginiv  {1.7em}
\if@twocolumn
  \setlength\leftmarginv  {.5em}
  \setlength\leftmarginvi {.5em}
\else
  \setlength\leftmarginv  {1em}
  \setlength\leftmarginvi {1em}
\fi
\setlength  \labelsep  {.5em}
\setlength  \labelwidth{\leftmargini}
\addtolength\labelwidth{-\labelsep}
\@beginparpenalty -\@lowpenalty
\@endparpenalty   -\@lowpenalty
\@itempenalty     -\@lowpenalty
%---------------------------------------------------------------
% Listennumerierung
%---------------------------------------------------------------
\renewcommand\theenumi{\@arabic\c@enumi}
\renewcommand\theenumii{\@alph\c@enumii}
\renewcommand\theenumiii{\@roman\c@enumiii}
\renewcommand\theenumiv{\@Alph\c@enumiv}
\newcommand\labelenumi{\theenumi.}
\newcommand\labelenumii{(\theenumii)}
\newcommand\labelenumiii{\theenumiii.}
\newcommand\labelenumiv{\theenumiv.}
\renewcommand\p@enumii{\theenumi}
\renewcommand\p@enumiii{\theenumi(\theenumii)}
\renewcommand\p@enumiv{\p@enumiii\theenumiii}
\newcommand\labelitemi{\textbullet}
\newcommand\labelitemii{\normalfont\bfseries \textendash}
\newcommand\labelitemiii{\textasteriskcentered}
\newcommand\labelitemiv{\textperiodcentered}
\newenvironment{description}
               {\list{}{\labelwidth\z@ \itemindent-\leftmargin
                        \let\makelabel\descriptionlabel}}
               {\endlist}
\newcommand*\descriptionlabel[1]{\hspace\labelsep
                                \normalfont\bfseries #1}
%---------------------------------------------------------------
% Umgebung: Quotation
%---------------------------------------------------------------
\newenvironment{quotation}
               {\list{}{\listparindent 1.5em%
                        \itemindent    \listparindent
                        \rightmargin   \leftmargin
                        \parsep        \z@ \@plus\p@}%
                \item\relax}
               {\endlist}
%---------------------------------------------------------------
% Umgebung: Quote
%---------------------------------------------------------------
\newenvironment{quote}
               {\list{}{\rightmargin\leftmargin}%
                \item\relax}
               {\endlist}
%---------------------------------------------------------------
% Umgebung: Titlepage
%---------------------------------------------------------------
\newenvironment{titlepage}                    {%
      \if@twocolumn
        \@restonecoltrue\onecolumn
      \else
%        Dies ist eine Dummyseite, damit rechts begonnen wird!
        \@restonecolfalse
%       \newpage
      \fi
      \thispagestyle{empty}%
%      \setcounter{page}\@ne
    }%
    {\if@restonecol\twocolumn \else \newpage \fi
     \if@twoside\else
%        \setcounter{page}\@ne
     \fi
    }
%---------------------------------------------------------------
% Umgebung: Appendix
%---------------------------------------------------------------
\newcommand\appendix{\par
  \setcounter{chapter}{0}%
  \setcounter{section}{0}%
  \gdef\@chapapp{\appendixname}%
%  \gdef\thechapter{\@Alph\c@chapter}}
  \gdef\thechapter{\@Alph\c@chapter}}
%---------------------------------------------------------------
% Abstände für Arrays und Tables
%---------------------------------------------------------------
\setlength\arraycolsep{5\p@}
\setlength\tabcolsep{6\p@}
\setlength\arrayrulewidth{.4\p@}
\setlength\doublerulesep{2\p@}
\setlength\tabbingsep{\labelsep}
\skip\@mpfootins = \skip\footins
\setlength\fboxsep{3\p@}
\setlength\fboxrule{.4\p@}
%---------------------------------------------------------------
% Numerierung: Equation
%---------------------------------------------------------------
\@addtoreset {equation}{chapter}
\renewcommand\theequation
  {\ifnum \c@chapter>\z@ \thechapter.\fi \@arabic\c@equation}
%---------------------------------------------------------------
% Numerierung: Figure
%---------------------------------------------------------------
\newcounter{figure}[chapter]
\renewcommand \thefigure
     {\ifnum \c@chapter>\z@ \thechapter.\fi \@arabic\c@figure}
\def\fps@figure{tbp}
\def\ftype@figure{1}
\def\ext@figure{lof}
\def\fnum@figure{\figurename~\thefigure}
\newenvironment{figure}
               {\@float{figure}}
               {\end@float}
\newenvironment{figure*}
               {\@dblfloat{figure}}
               {\end@dblfloat}
%---------------------------------------------------------------
% Numerierung: Table
%---------------------------------------------------------------
\newcounter{table}[chapter]
\renewcommand \thetable
     {\ifnum \c@chapter>\z@ \thechapter.\fi \@arabic\c@table}
\def\fps@table{tbp}
\def\ftype@table{2}
\def\ext@table{lot}
\def\fnum@table{\tablename~\thetable}
\newenvironment{table}
               {\@float{table}}
               {\end@float}
\newenvironment{table*}
               {\@dblfloat{table}}
               {\end@dblfloat}
%---------------------------------------------------------------
% Captions (aus dem Caption-Package, bf, isu, nooneline)
%---------------------------------------------------------------
\newlength\abovecaptionskip
\newlength\belowcaptionskip
\setlength\abovecaptionskip{4\p@}
\setlength\belowcaptionskip{4\p@}
\newlength\captionmargin
\setlength\captionmargin{0\p@}
\newsavebox{\as@captionbox}
\newlength{\as@captionwidth}
\newcommand{\as@isucaption}[2]{
  \sbox{\as@captionbox}{#1\space}
  \addtolength{\as@captionwidth}{-\wd\as@captionbox}
  \usebox{\as@captionbox}\parbox[t]{\as@captionwidth}{\leavevmode#2}}
\newcommand{\as@makecaption}[2]{
  \setlength{\leftskip}{\captionmargin}
  \setlength{\rightskip}{\captionmargin}
  \addtolength{\as@captionwidth}{-2\captionmargin}
  \as@isucaption{\captionfont \textbf{#1:}}{\captionfont #2}}
\newcommand{\@makecaption}[2]{
  \vskip\abovecaptionskip
  \setlength{\as@captionwidth}{\linewidth}
  \as@makecaption{#1}{#2}
  \vskip\belowcaptionskip}
%---------------------------------------------------------------
% Captions von Gleitumgebungen in anderer Schriftgröße/-art (Lars)
%---------------------------------------------------------------
\newcommand\captionfont{\normalsize}  
%---------------------------------------------------------------
% Alte Schriftkommandos
%---------------------------------------------------------------
\DeclareOldFontCommand{\rm}{\normalfont\rmfamily}{\mathrm}
\DeclareOldFontCommand{\sf}{\normalfont\sffamily}{\mathsf}
\DeclareOldFontCommand{\tt}{\normalfont\ttfamily}{\mathtt}
\DeclareOldFontCommand{\bf}{\normalfont\bfseries}{\mathbf}
\DeclareOldFontCommand{\it}{\normalfont\itshape}{\mathit}
\DeclareOldFontCommand{\sl}{\normalfont\slshape}{\@nomath\sl}
\DeclareOldFontCommand{\sc}{\normalfont\scshape}{\@nomath\sc}
\DeclareRobustCommand*\cal{\@fontswitch\relax\mathcal}
\DeclareRobustCommand*\mit{\@fontswitch\relax\mathnormal}
%---------------------------------------------------------------
% Inhaltsverzeichnis
%---------------------------------------------------------------
\newcommand\@pnumwidth{1.55em}
\newcommand\@tocrmarg{2.55em}
\newcommand\@dotsep{4.5}
\newlength\@docparskip
\newlength\tocparskip
\setlength\tocparskip{0\p@}
%\setcounter{tocdepth}{4}
\setcounter{tocdepth}{3}
\newcommand\tableofcontents{%
    \if@twocolumn
      \@restonecoltrue\onecolumn
    \else
      \@restonecolfalse
    \fi
    \chapter*{\contentsname
        \@mkboth{%
           \headertextfont \contentsname}{\contentsname}}%
    \addcontentsline{toc}{chapter}{\contentsname}%
    \setlength\@docparskip\parskip
    \setlength\parskip\tocparskip
    \@starttoc{toc}%
    \setlength\parskip\@docparskip
    \if@restonecol\twocolumn\fi
    }
\newcommand*\l@part[2]{%
  \ifnum \c@tocdepth >-2\relax
    \addpenalty{-\@highpenalty}%
    \addvspace{2.25em \@plus\p@}%
    \begingroup
      \parindent \z@ \rightskip \@pnumwidth
      \parfillskip -\@pnumwidth
      {\leavevmode
       \large \bfseries #1\hfil \hb@xt@\@pnumwidth{\hss #2}}\par
       \nobreak
         \global\@nobreaktrue
         \everypar{\global\@nobreakfalse\everypar{}}%
    \endgroup
  \fi}
\newcommand*\l@chapter[2]{%
  \ifnum \c@tocdepth >\m@ne
    \addpenalty{-\@highpenalty}%
    \vskip 1.0em \@plus\p@
    \setlength\@tempdima{1.5em}%
    \begingroup
      \parindent \z@ \rightskip \@pnumwidth
      \parfillskip -\@pnumwidth
      \leavevmode \bfseries
      \advance\leftskip\@tempdima
      \hskip -\leftskip
      #1\nobreak\hfil \nobreak\hb@xt@\@pnumwidth{\hss #2}\par
      \penalty\@highpenalty
    \endgroup
  \fi}
\newcommand*\l@section{\@dottedtocline{1}{1.5em}{2.3em}}
\newcommand*\l@subsection{\@dottedtocline{2}{3.8em}{3.2em}}
\newcommand*\l@subsubsection{\@dottedtocline{3}{7.0em}{4.1em}}
\newcommand*\l@paragraph{\@dottedtocline{4}{10em}{5em}}
\newcommand*\l@subparagraph{\@dottedtocline{5}{12em}{6em}}
%---------------------------------------------------------------
% Figure-Verzeichnis
%---------------------------------------------------------------
\newcommand\listoffigures{%
    \if@twocolumn
      \@restonecoltrue\onecolumn
    \else
      \@restonecolfalse
    \fi
    \chapter*{\listfigurename
      \@mkboth{\listfigurename}%
              {\listfigurename}}%
    \addcontentsline{toc}{chapter}{\listfigurename}%
    \@starttoc{lof}%
    \if@restonecol\twocolumn\fi
    }
\newcommand*\l@figure{\@dottedtocline{1}{1.5em}{2.3em}}
%---------------------------------------------------------------
% Table-Verzeichnis
%---------------------------------------------------------------
\newcommand\listoftables{%
    \if@twocolumn
      \@restonecoltrue\onecolumn
    \else
      \@restonecolfalse
    \fi
    \chapter*{\listtablename
      \@mkboth{%
          \listtablename}{\listtablename}}%
    \addcontentsline{toc}{chapter}{\listtablename}%
    \@starttoc{lot}%
    \if@restonecol\twocolumn\fi
    }
\let\l@table\l@figure


%---------------------------------------------------------------
% Literaturverzeichnis
%---------------------------------------------------------------
\newdimen\bibindent
\setlength\bibindent{1.5em}
\newenvironment{thebibliography}[1]{
% Lars:
%  \chapter*{\bibname \@mkboth{\bibname}{\bibname}}%
  \chapter*{\bibname \@mkboth{\headertextfont \bibname}{\bibname}}%
  \addcontentsline{toc}{chapter}{\bibname}
  \list{\@biblabel{\@arabic\c@enumiv}}%
   {\settowidth\labelwidth{\@biblabel{#1}}%
    \leftmargin\labelwidth
    \advance\leftmargin\labelsep
    \@openbib@code
    \usecounter{enumiv}%
    \let\p@enumiv\@empty
    \renewcommand\theenumiv{\@arabic\c@enumiv}}%
  \sloppy
% Strafpunkte für Seitentrennung nach erster bzw. vor letzter Zeile eines Absatzes
  \clubpenalty=10000
  \@clubpenalty \clubpenalty
  \widowpenalty=10000%
  \sfcode`\.\@m}

\newenvironment{thebibliographyweitere}[1]{
% Lars:
  \list{\@biblabel{\@arabic\c@enumiv}}%
   {\settowidth\labelwidth{\@biblabel{#1}}%
    \leftmargin\labelwidth
    \advance\leftmargin\labelsep
    \@openbib@code
    \usecounter{enumiv}%
    \let\p@enumiv\@empty
    \renewcommand\theenumiv{\@arabic\c@enumiv}}%
  \sloppy
% Strafpunkte für Seitentrennung nach erster bzw. vor letzter Zeile eines Absatzes
  \clubpenalty=10000
  \@clubpenalty \clubpenalty
  \widowpenalty=10000%
  \sfcode`\.\@m}

   {\def\@noitemerr
     {\@latex@warning{Empty `thebibliography' environment}}%
    \endlist}
\newcommand\newblock{\hskip .11em\@plus.33em\@minus.07em}
\let\@openbib@code\@empty
%---------------------------------------------------------------
% Index
%---------------------------------------------------------------
\newenvironment{theindex}
               {\if@twocolumn
                  \@restonecolfalse
                \else
                  \@restonecoltrue
                \fi
                \columnseprule \z@
                \columnsep 35\p@
                \twocolumn[\@makeschapterhead{\indexname}]%
                \@mkboth{\indexname}%
                        {\indexname}%
                \thispagestyle{plain}\parindent\z@
                \parskip\z@ \@plus .3\p@\relax
                \let\item\@idxitem}
               {\if@restonecol\onecolumn\else\clearpage\fi}
\newcommand\@idxitem{\par\hangindent 40\p@}
\newcommand\subitem{\@idxitem \hspace*{20\p@}}
\newcommand\subsubitem{\@idxitem \hspace*{30\p@}}
\newcommand\indexspace{\par \vskip 10\p@ \@plus5\p@ \@minus3\p@\relax}
%---------------------------------------------------------------
% Fußnotenlinie neu definieren
%---------------------------------------------------------------
\renewcommand\footnoterule{%
  \kern-3\p@
  \hrule\@width.4\columnwidth
  \kern2.6\p@}
\@addtoreset{footnote}{chapter}
%---------------------------------------------------------------
% ???
%---------------------------------------------------------------
\newcommand\@makefntext[1]{%
    \parindent 1em%
    \noindent
    \hb@xt@1.8em{\hss\@makefnmark}#1}
%---------------------------------------------------------------
% Diverse Texte (werden von ngerman.sty überschrieben!) 
% Lars: wirklich? Ja, wenn \usepackage{ngerman} nach \documentclass verwendet wird! 
% Sonst nicht!!! (Besser hier umdefinieren!)
%---------------------------------------------------------------
\newcommand\contentsname{Inhalt}
\newcommand\listfigurename{Bildverzeichnis}
\newcommand\listtablename{Tabellenverzeichnis}

\newcommand\bibname{Literatur}
\newcommand\indexname{Index}
\newcommand\figurename{Bild}
\newcommand\tablename{Tabelle}
\newcommand\partname{Hauptteil}
\newcommand\chaptername{Kapitel}
\ifngerman
\newcommand\losname{Formelverzeichnis}
\newcommand\cvname{Lebenslauf}
\newcommand\appendixname{Anhang}
\else
\newcommand\losname{List of Symbols and Abbreviations}
%\newcommand\cvname{Curriculum Vitae}
\newcommand\appendixname{Appendix}
\fi
\newcommand\abstractname{Kurzfassung}
\def\today{\ifcase\month\or
  January\or February\or March\or April\or May\or June\or
  July\or August\or September\or October\or November\or December\fi
  \space\number\day, \number\year}
%---------------------------------------------------------------
% Seite einrichten
%---------------------------------------------------------------
\pagestyle{headings}
\pagenumbering{arabic}
\raggedbottom
\sloppy

%---------------------------------------------------------------
% Neue rechte Seite beginnen, dabei auf evtl. freier Seite 
% nur die Seitennummer
%---------------------------------------------------------------
\newcommand\openright{
    \clearpage
    \thispagestyle{firsthead}
    \cleardoublepage
}
%---------------------------------------------------------------
% Ergänzungen 
%---------------------------------------------------------------
\newcommand{\cleardoublepageempty}{%
  \clearpage%
  \if@twoside\ifodd\c@page\else\hbox{}\thispagestyle{empty}\clearpage\fi\fi}
\newcommand{\startnewpage}{\if@openright\cleardoublepageempty\else\clearpage\fi}

\newif\if@mainmatter \@mainmattertrue
\newcommand\frontmatter{\cleardoublepageempty
            \@mainmatterfalse
%            \if@twoside\setcounter{page}{3} \ifdatitelseite \addtocounter{page}{2}\fi \ifda \addtocounter{page}{2}\fi
%            \else\setcounter{page}{2} \ifdatitelseite \addtocounter{page}{1} \fi \ifda \addtocounter{page}{1}\fi\fi          
            }
%
\newcommand\mainmatter{\cleardoublepageempty
       \@mainmattertrue\pagenumbering{arabic}}
%
\newcommand\backmatter{\clearpage\@mainmatterfalse}
%---------------------------------------------------------------
% Formelzeichen
%---------------------------------------------------------------
\newenvironment{formelzeichen}
  {\chapter*{\losname}
  \thispagestyle{kapitelbeginn}
  \addcontentsline{toc}{chapter}{\losname}
  \markboth{\headertextfont \losname}{\losname}}
  {\newpage}  
%---------------------------------------------------------------
% Umgebung: Widmung (kursive Schrift)
%---------------------------------------------------------------
\newenvironment{widmung}
               {\begin{center}\thispagestyle{kapitelbeginn}\vspace*{10cm}\itshape}
               {\end{center}\cleardoublepage\rmfamily}           
%---------------------------------------------------------------
% Umgebung: Abstract (automatische zeitweise Umschaltung auf englische Trennmuster)
%---------------------------------------------------------------
\newenvironment{abstract}
               {\ifx\selectlanguage\undefined\else\selectlanguage{USenglish}\fi \chapter*{Abstract}
                \addcontentsline{toc}{chapter}{Abstract}
                \thispagestyle{kapitelbeginn}}
               {\ifusenglish\ifx\selectlanguage\undefined\else\selectlanguage{USenglish}\fi
               \else\ifx\selectlanguage\undefined\else\selectlanguage{ngerman}\fi\fi}

\newenvironment{zusammenfassung}
               {\ifx\selectlanguage\undefined\else\selectlanguage{USenglish}\fi \chapter*{Zusammenfassung}
                \addcontentsline{toc}{chapter}{Zusammenfassung}
                \thispagestyle{kapitelbeginn}}
               {\ifusenglish\ifx\selectlanguage\undefined\else\selectlanguage{USenglish}\fi
               \else\ifx\selectlanguage\undefined\else\selectlanguage{ngerman}\fi\fi}
%---------------------------------------------------------------
% Umgebung: Kurzfassung (automatische zeitweise Umschaltung auf neue deutsche Trennmuster)
%---------------------------------------------------------------
\newenvironment{kurzfassung}
               {\ifx\selectlanguage\undefined\else\selectlanguage{ngerman}\fi \chapter*{Kurzfassung}
                \addcontentsline{toc}{chapter}{Kurzfassung}
                \thispagestyle{kapitelbeginn}}
               {\ifusenglish\ifx\selectlanguage\undefined\else\selectlanguage{USenglish}\fi
               \else\ifx\selectlanguage\undefined\else\selectlanguage{ngerman}\fi\fi}
%---------------------------------------------------------------
% Umgebung: Vorwort 
%---------------------------------------------------------------
\newenvironment{vorwort}[1]
               {\chapter*{#1}}
               {\newpage}  
%---------------------------------------------------------------
% Umgebung: Aufgabenstellung
%---------------------------------------------------------------
\newenvironment{aufgabenstellung}
               {\chapter*{\vspace*{-20mm}Task Description}\thispagestyle{empty}}
               {\vfill \iatreferentdrei \\ Berlin, \iatausgabedatum \cleardoublepageempty}  
%---------------------------------------------------------------
% Umgebung: Erklärung
%---------------------------------------------------------------
\newenvironment{erklaerung}
                {\chapter*{\vspace*{-20mm}Declaration }\thispagestyle{empty}}
               {\vspace*{5cm}\\\\Berlin,  \iatpromotionstag.~\iatpromotionsmonat~\iatpromotionsjahr \\ \vspace{2cm}  \\\\ \makebox[2.5in]{\hrulefill}\\  \iatverfasser  \cleardoublepageempty} \newpage 




           %    {\cleardoublepageempty\chapter*{\vspace*{-20mm}Erklärung}\thispagestyle{empty}\vfill}
            %   {\vspace*{3cm}\\\iatverfasser\\Berlin, den \iatpromotionstag.~\iatpromotionsmonat~\iatpromotionsjahr\cleardoublepageempty}  
%---------------------------------------------------------------
% Umgebung: Lebenslauf  
%---------------------------------------------------------------
\newenvironment{lebenslauf}
               {
               \chapter*{\vspace*{-20mm}\cvname} 
               \pagestyle{empty} }
               {}    
%---------------------------------------------------------------
% Umgebung: Anhang 
%---------------------------------------------------------------
\newenvironment{anhang}
               {\addcontentsline{toc}{chapter}{\appendixname}
               \begin{appendix} 
                \thispagestyle{kapitelbeginn} \newcommand{\defchapter}{\chapter} \renewcommand{\chapter}{\chaptera}\headers{\appendixname}}
               {\renewcommand{\chapter}{\defchapter}
               \end{appendix}}
%---------------------------------------------------------------
% Definitionen für Unterverzeichnisstruktur
%---------------------------------------------------------------
% Name des aktuellen Unterverzeichnisses
\newcommand\chaptersubdir{}
\newcommand\newchaptersubdir{}
%
% Kapiteldatei aus Unterverzeichnis einbinden
\newcommand\includefile[2]{\renewcommand{\chaptersubdir}{#1}\input{#1/#2}}
%
% Weitere Datei aus aktuellem Unterverzeichnis einbinden
\newcommand\includesubfile[2]{\renewcommand{\newchaptersubdir}{\chaptersubdir/#1/Bilder}\input{\chaptersubdir/#1/#2}}
%

\newcommand{\headertextfont}{\small \scshape \rmfamily \let\uppercase\relax}
\newcommand{\headerpagefont}{\normalsize \scshape \rmfamily \let\uppercase\relax}


%---------------------------------------------------------------
% Dateiende
%---------------------------------------------------------------
\endinput
%%
%% End of file `diss.cls'.
