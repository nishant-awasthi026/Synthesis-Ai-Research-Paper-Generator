"""
Add Sample Research Papers to the RAG Database
Run this to test the similarity search and RAG features
"""
import sys
sys.path.insert(0, ".")

from backend.rag.vector_store import get_vector_store

def add_sample_papers():
    """Add a collection of famous AI/ML research papers"""
    
    papers = [
        {
            "id": "paper_attention",
            "title": "Attention Is All You Need",
            "abstract": "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely.",
            "authors": ["Vaswani", "Shazeer", "Parmar", "Uszkoreit", "Jones", "Gomez", "Kaiser", "Polosukhin"],
            "year": "2017",
            "source": "arxiv",
            "niches": ["Deep Learning", "NLP", "Transformers"],
            "doi": "10.48550/arXiv.1706.03762",
            "url": "https://arxiv.org/abs/1706.03762"
        },
        {
            "id": "paper_bert",
            "title": "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding",
            "abstract": "We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers. Unlike recent language representation models, BERT is designed to pre-train deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers.",
            "authors": ["Devlin", "Chang", "Lee", "Toutanova"],
            "year": "2018",
            "source": "arxiv",
            "niches": ["NLP", "Deep Learning", "Language Models"],
            "doi": "10.48550/arXiv.1810.04805",
            "url": "https://arxiv.org/abs/1810.04805"
        },
        {
            "id": "paper_resnet",
            "title": "Deep Residual Learning for Image Recognition",
            "abstract": "Deeper neural networks are more difficult to train. We present a residual learning framework to ease the training of networks that are substantially deeper than those used previously. We explicitly reformulate the layers as learning residual functions with reference to the layer inputs, instead of learning unreferenced functions.",
            "authors": ["He", "Zhang", "Ren", "Sun"],
            "year": "2015",
            "source": "arxiv",
            "niches": ["Computer Vision", "Deep Learning", "CNN"],
            "doi": "10.48550/arXiv.1512.03385",
            "url": "https://arxiv.org/abs/1512.03385"
        },
        {
            "id": "paper_gan",
            "title": "Generative Adversarial Networks",
            "abstract": "We propose a new framework for estimating generative models via an adversarial process, in which we simultaneously train two models: a generative model G that captures the data distribution, and a discriminative model D that estimates the probability that a sample came from the training data rather than G.",
            "authors": ["Goodfellow", "Pouget-Abadie", "Mirza", "Xu", "Warde-Farley", "Ozair", "Courville", "Bengio"],
            "year": "2014",
            "source": "arxiv",
            "niches": ["Deep Learning", "Generative Models", "Computer Vision"],
            "doi": "10.48550/arXiv.1406.2661",
            "url": "https://arxiv.org/abs/1406.2661"
        },
        {
            "id": "paper_adam",
            "title": "Adam: A Method for Stochastic Optimization",
            "abstract": "We introduce Adam, an algorithm for first-order gradient-based optimization of stochastic objective functions, based on adaptive estimates of lower-order moments. The method is straightforward to implement, is computationally efficient, has little memory requirements, is invariant to diagonal rescaling of the gradients, and is well suited for problems that are large in terms of data and/or parameters.",
            "authors": ["Kingma", "Ba"],
            "year": "2014",
            "source": "arxiv",
            "niches": ["Optimization", "Deep Learning", "Machine Learning"],
            "doi": "10.48550/arXiv.1412.6980",
            "url": "https://arxiv.org/abs/1412.6980"
        },
        {
            "id": "paper_dropout",
            "title": "Dropout: A Simple Way to Prevent Neural Networks from Overfitting",
            "abstract": "Deep neural nets with a large number of parameters are very powerful machine learning systems. However, overfitting is a serious problem in such networks. Large networks are also slow to use, making it difficult to deal with overfitting by combining the predictions of many different large neural nets at test time. Dropout is a technique for addressing this problem.",
            "authors": ["Srivastava", "Hinton", "Krizhevsky", "Sutskever", "Salakhutdinov"],
            "year": "2014",
            "source": "jmlr",
            "niches": ["Deep Learning", "Regularization", "Machine Learning"],
            "doi": "JMLR.15.1929",
            "url": "https://jmlr.org/papers/v15/srivastava14a.html"
        },
        {
            "id": "paper_vit",
            "title": "An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale",
            "abstract": "While the Transformer architecture has become the de-facto standard for natural language processing tasks, its applications to computer vision remain limited. In vision, attention is either applied in conjunction with convolutional networks, or used to replace certain components of convolutional networks while keeping their overall structure in place. We show that this reliance on CNNs is not necessary.",
            "authors": ["Dosovitskiy", "Beyer", "Kolesnikov", "Weissenborn", "Zhai", "Unterthiner"],
            "year": "2020",
            "source": "arxiv",
            "niches": ["Computer Vision", "Transformers", "Deep Learning"],
            "doi": "10.48550/arXiv.2010.11929",
            "url": "https://arxiv.org/abs/2010.11929"
        },
        {
            "id": "paper_gpt3",
            "title": "Language Models are Few-Shot Learners",
            "abstract": "Recent work has demonstrated substantial gains on many NLP tasks and benchmarks by pre-training on a large corpus of text followed by fine-tuning on a specific task. While typically task-agnostic in architecture, this method still requires task-specific fine-tuning datasets of thousands or tens of thousands of examples. We demonstrate that scaling up language models greatly improves task-agnostic, few-shot performance.",
            "authors": ["Brown", "Mann", "Ryder", "Subbiah", "Kaplan"],
            "year": "2020",
            "source": "arxiv",
            "niches": ["NLP", "Language Models", "Few-Shot Learning"],
            "doi": "10.48550/arXiv.2005.14165",
            "url": "https://arxiv.org/abs/2005.14165"
        },
        {
            "id": "paper_unet",
            "title": "U-Net: Convolutional Networks for Biomedical Image Segmentation",
            "abstract": "There is large consent that successful training of deep networks requires many thousand annotated training samples. In this paper, we present a network and training strategy that relies on the strong use of data augmentation to use the available annotated samples more efficiently. The architecture consists of a contracting path to capture context and a symmetric expanding path that enables precise localization.",
            "authors": ["Ronneberger", "Fischer", "Brox"],
            "year": "2015",
            "source": "arxiv",
            "niches": ["Computer Vision", "Medical Imaging", "Segmentation"],
            "doi": "10.48550/arXiv.1505.04597",
            "url": "https://arxiv.org/abs/1505.04597"
        },
        {
            "id": "paper_alphago",
            "title": "Mastering the game of Go with deep neural networks and tree search",
            "abstract": "The game of Go has long been viewed as the most challenging of classic games for artificial intelligence owing to its enormous search space and the difficulty of evaluating board positions and moves. Here we introduce a new approach to computer Go that uses 'value networks' to evaluate board positions and 'policy networks' to select moves.",
            "authors": ["Silver", "Huang", "Maddison", "Guez", "Sifre", "van den Driessche"],
            "year": "2016",
            "source": "nature",
            "niches": ["Reinforcement Learning", "Deep Learning", "Game AI"],
            "doi": "10.1038/nature16961",
            "url": "https://www.nature.com/articles/nature16961"
        }
    ]
    
    print("🚀 Adding Sample Research Papers to RAG Database")
    print("="*60)
    
    try:
        # Get vector store
        print("\n📦 Initializing vector store...")
        vs = get_vector_store()
        
        # Check current count
        current_count = vs.count()
        print(f"📊 Current papers in database: {current_count}")
        
        # Add papers
        print(f"\n📝 Adding {len(papers)} papers...")
        added = vs.add_papers(papers)
        
        new_count = vs.count()
        
        print(f"✅ Successfully added {added} papers!")
        print(f"📊 Total papers in database: {new_count}")
        
        # Test similarity search
        print("\n" + "="*60)
        print("🔍 Testing Similarity Search")
        print("="*60)
        
        query = "neural network optimization and training efficiency"
        print(f"\nQuery: '{query}'")
        print("\nTop 3 most similar papers:")
        
        similar = vs.search_similar(query, top_k=3)
        
        for i, paper in enumerate(similar, 1):
            print(f"\n{i}. {paper['title']}")
            print(f"   Authors: {paper.get('authors', 'N/A')}")
            print(f"   Year: {paper.get('year', 'N/A')}")
            print(f"   Similarity: {paper['similarity_score']:.3f}")
            print(f"   Niches: {paper.get('niches', 'N/A')}")
        
        print("\n" + "="*60)
        print("🎉 Setup Complete!")
        print("="*60)
        print("\n✅ RAG database is ready for use!")
        print("\n💡 Next steps:")
        print("   1. Test similarity search in API: /api/discovery/similar")
        print("   2. Try novelty detection: /api/discovery/novelty")
        print("   3. Generate with RAG context: use_rag=true in /api/generate/section")
        print("\n📚 API Docs: http://localhost:8000/docs\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure:")
        print("  1. Virtual environment is activated")
        print("  2. Dependencies are installed")
        print("  3. Server is running")

if __name__ == "__main__":
    add_sample_papers()
