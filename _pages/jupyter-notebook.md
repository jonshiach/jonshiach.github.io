---
title: "Jupyter notebooks"
permalink: /jupyter-notebook/
author_profile: true
---

{% include toc %}

Jupyter notebooks combine text and code which makes it possible to produce readable documents that includes Python code. I use Jupyter in my teaching and outreach events since it gives users the ability to experiment with coding in an accessible way.

# Installing Jupyter 

To run or create a notebook you will first need to make sure you have Jupyter installed on your computer. The easiest way to do this is to download and install [Anaconda](https://www.anaconda.com/) which is a suite of mathematical and scientific software applications.

1. Go to [www.anaconda.com](https://www.anaconda.com/) and click on the download link. This should download the appropriate installer for your operating system.
2. Install Anaconda onto your computer. In most instances the default installation options will suffice. Note that you may need administration privileges to install Anaconda.

# Using notebooks

To open a notebook file in Jupyter we first need to run the Jupyter application.

1. Run Jupyter by doing the following
    - Windows: click on the start menu button and type `jupyter`. This should locate the Jupyter application which can be run by pressing enter.
    - macOS/Linux: open a terminal window and enter `jupyter notebook`. Alternatively run **Anaconda Navigator** and select **Juypter notebook**.

2. Using the file browser which should have opened in your web browser, navigate to the notebook you downloaded and click on it. This should open the Jupyter notebook application.

Once the notebook has opened you should be presented with some text and code in a browser window.

<p style="text-align: center"><img src="/images/notebook1.png" width="700" /></p>

The content of a notebook is contained in **cells**. Text is contained in **[markdown](https://www.markdownguide.org/basic-syntax/) cells** which can be used to display rich text, graphics and tables. Code is contained in **code cells** in which we can enter Python code and execute it. To execute all cells in a notebook click on the 'run all' button at the top of the page. To run an individual cell click on the cell and click on the 'run' button. Alternatively pressing `ctrl` and `enter` keys will run the currently selected cell.

<p style="text-align: center"><img src="/images/notebook2.png" width="700" /></p>

# Google Colab

If you are unable to install Jupyter on your computer you can run Jupyter notebooks in the cloud using [Google Colab](https://colab.research.google.com/). To do this you will need to have a [Google account](https://www.google.com/account/about/).

1. If you already have a Google account skip this step. Go to [https://www.google.com/account/about/](https://www.google.com/account/about/) and sign up for a Google account.
1. Go to [https://colab.research.google.com/](https://colab.research.google.com/) and log into your Google account.
1. Click on **Upload** and upload the notebook you have downloaded.
1. Click on **Runtime** and **Run all** to run the notebook
    <p style="text-align: center"><img src="/images/colab1.png" width="700" /></p>
1. To run an individual code cell click on it and then click on the play button to the left of the cell.
    <p style="text-align: center"><img src="/images/colab2.png" width="700" /></p>
