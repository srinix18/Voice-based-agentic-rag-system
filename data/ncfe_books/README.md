# Sample PDFs Guide

This directory should contain PDF files from NCFE's e-Library (https://ncfe.org.in/e-library/).

## How to Add PDFs

1. Download PDF files from NCFE e-Library
2. Copy them to this directory (`data/ncfe_books/`)
3. The system will automatically process them on first run

## Recommended Content

For a financial literacy agent, consider including PDFs on:

- Basic financial concepts (savings, investments, interest)
- Banking and financial institutions
- Stock markets and SEBI regulations
- Insurance and risk management
- Personal finance and budgeting
- Economic concepts (inflation, GDP, etc.)
- Mutual funds and securities
- Financial planning and retirement

## Processing

When you run the agent:

1. All PDFs in this directory will be loaded
2. Text will be extracted from each page
3. Content will be chunked into searchable segments
4. Embeddings will be created for semantic search
5. A FAISS index will be cached for fast retrieval

## File Requirements

- **Format**: PDF (.pdf)
- **Content**: Text-based (not scanned images)
- **Language**: English recommended
- **Size**: No strict limit, but larger files take longer to process

## Example Structure

```
ncfe_books/
├── financial_literacy_basics.pdf
├── sebi_regulations.pdf
├── banking_system.pdf
├── investment_guide.pdf
└── personal_finance.pdf
```

## Notes

- The first run may take a few minutes to index all PDFs
- Subsequent runs will use a cached index (faiss_index.pkl)
- To rebuild the index, delete the cache file or use `rebuild_index()`
- More PDFs = better coverage but slower initial indexing

---

**Ready to start?** Add your PDF files here and run `python demo.py` to test!
