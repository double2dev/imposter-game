# Imposter Game Words Dataset & Tools

[![Website Status](https://img.shields.io/website?url=https%3A%2F%2Fimpostergamewords.com&up_message=online&down_message=offline&label=ImposterGameWords.com)](https://impostergamewords.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](CONTRIBUTING.md)

Welcome to the official open-source repository for **[Imposter Game Words](https://impostergamewords.com)**! 

This repository serves as the central hub for our community dataset, internal maintenance tools, and public issue tracker. Our mission is to provide the most balanced, creative, and fun word pairs for social deduction games like Imposter, Spyfall, and Chameleon.

> 🎮 **Want to play right now?**
> You don't need to download anything! Play the ultimate Imposter game instantly in your browser at **[ImposterGameWords.com](https://impostergamewords.com)**. It works perfectly on mobile, tablets, and desktop.

---

## 📚 What's in this Repository?

To keep our core web application secure and optimized, we keep our front-end UI and serverless functions closed-source. However, we believe the **content** and the **tools** should be community-driven. 

This repository contains:

1. **`dataset/`**: The open-source `JSON` datasets of word pairs used in our game engine.
2. **`tools/`**: Python utility scripts we use for site generation, CI/CD, and link checking.
3. **Issue Tracker**: The official place to report bugs on the main website or suggest new features.

## 🎲 The Dataset (`dataset/imposter_words_v1.json`)

Creating a balanced game requires carefully curated word pairs. If the words are too similar (e.g., *Car / Automobile*), the Imposter wins too easily. If they are too different (e.g., *Car / Banana*), the Civilians win immediately.

Our dataset categorizes words into distinct editions:
- **Standard**: General knowledge, perfect for mixed groups.
- **Kids**: Family-safe, concrete nouns.
- **Couples**: Spicy and relationship-focused.
- **Tech / Office**: Perfect for Zoom calls and coworkers.

Feel free to use this dataset in your own non-commercial projects!

## 🤝 How to Contribute

We love community contributions! There are two main ways you can help:

### 1. Suggest New Word Pairs
Have a great idea for a tricky word pair? We want to hear it! 
- Go to our [Issues tab](../../issues)
- Select the **"New Word Suggestion"** template
- Fill out the details. If it's a great fit, we'll add it to the live database on [ImposterGameWords.com](https://impostergamewords.com).

### 2. Report a Bug
If you found a broken link, a typo on the website, or an issue with the online generator:
- Open a **"Bug Report"** in our Issues tab.
- Our maintainers will address it in the next deployment cycle.

For more detailed instructions, please read our [Contributing Guidelines](CONTRIBUTING.md).

## 🛠️ Included Tools

In the `tools/` directory, you'll find scripts we use to maintain the site. 
- `check_links.py`: A robust Python script that crawls static HTML directories to ensure zero 404 dead links (both internal and external).
- `build_pages.py`: Our templating script for generating static SEO pages.

## 📜 Code of Conduct

We are committed to providing a welcoming and inspiring community for all. Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before participating in this project.

## 📄 License

The datasets and scripts in this repository are licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

---
*Built with ❤️ for party gamers everywhere.*
