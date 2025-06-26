#!/usr/bin/env python3
"""
Retrieval Latency Benchmark
Measures vector search performance at different corpus sizes
"""

import sys
import time
import json
import argparse
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from rag_system import RAGSystem
from rag_system.document_processor import DocumentProcessor

def generate_test_corpus(size: int) -> list[str]:
    """Generate synthetic documents for benchmarking"""
    
    # Base templates for different document types
    templates = [
        "The capital of {country} is {city}. It has a population of {pop} million people.",
        "Company policy states that {topic} should be handled by {department}. Contact {email} for details.",
        "To troubleshoot {issue}, first check {step1}, then verify {step2}, and finally {step3}.",
        "Research shows that {technology} improves {metric} by {percentage}% in {domain} applications.",
        "The {product} specification includes {feature1}, {feature2}, and {feature3} capabilities."
    ]
    
    # Sample data pools
    countries = ["France", "Germany", "Japan", "Brazil", "Canada", "Australia", "India", "China"]
    cities = ["Paris", "Berlin", "Tokyo", "Brasilia", "Ottawa", "Canberra", "Delhi", "Beijing"]
    topics = ["vacation requests", "expense reports", "project approvals", "sick leave", "training"]
    departments = ["HR", "Finance", "IT", "Legal", "Operations"]
    issues = ["API errors", "slow queries", "connection timeouts", "authentication failures"]
    technologies = ["machine learning", "neural networks", "deep learning", "transformers"]
    domains = ["healthcare", "finance", "retail", "manufacturing", "education"]
    
    documents = []
    for i in range(size):
        template = templates[i % len(templates)]
        
        if "capital" in template:
            doc = template.format(
                country=countries[i % len(countries)],
                city=cities[i % len(cities)],
                pop=np.random.randint(1, 20)
            )
        elif "policy" in template:
            doc = template.format(
                topic=topics[i % len(topics)],
                department=departments[i % len(departments)],
                email=f"support-{i}@company.com"
            )
        elif "troubleshoot" in template:
            doc = template.format(
                issue=issues[i % len(issues)],
                step1="system logs",
                step2="network connectivity", 
                step3="service status"
            )
        elif "research" in template:
            doc = template.format(
                technology=technologies[i % len(technologies)],
                metric="accuracy",
                percentage=np.random.randint(10, 50),
                domain=domains[i % len(domains)]
            )
        else:
            doc = template.format(
                product=f"Product-{i}",
                feature1="high performance",
                feature2="scalability",
                feature3="reliability"
            )
            
        documents.append(f"Document {i+1}: {doc}")
    
    return documents

def benchmark_retrieval_latency(corpus_sizes: list[int], num_queries: int = 10) -> dict:
    """Benchmark retrieval latency across different corpus sizes"""
    
    results = {
        'corpus_sizes': corpus_sizes,
        'avg_latency_ms': [],
        'p95_latency_ms': [],
        'throughput_qps': []
    }
    
    test_queries = [
        "What is the capital of France?",
        "How do I handle vacation requests?", 
        "How to troubleshoot API errors?",
        "What research shows about machine learning?",
        "What are the product specifications?"
    ]
    
    for size in corpus_sizes:
        print(f"\n📊 Benchmarking corpus size: {size:,} documents")
        
        # Generate test corpus
        print("📄 Generating test documents...")
        documents = generate_test_corpus(size)
        
        # Save to temporary files
        temp_dir = Path("temp_benchmark_docs")
        temp_dir.mkdir(exist_ok=True)
        
        for i, doc in enumerate(documents):
            (temp_dir / f"doc_{i:06d}.txt").write_text(doc, encoding='utf-8')
        
        try:
            # Initialize RAG system
            print("🔧 Building vector index...")
            start_build = time.time()
            
            rag = RAGSystem()
            # Override documents directory temporarily
            rag.documents_dir = temp_dir
            rag.load_documents()
            rag.build_index()
            
            build_time = time.time() - start_build
            print(f"⚡ Index built in {build_time:.2f}s")
            
            # Run queries and measure latency
            print(f"🧪 Running {num_queries} test queries...")
            latencies = []
            
            for i in range(num_queries):
                query = test_queries[i % len(test_queries)]
                
                start_query = time.time()
                response = rag.query(query)
                query_time = (time.time() - start_query) * 1000  # Convert to ms
                
                latencies.append(query_time)
                print(f"  Query {i+1}: {query_time:.1f}ms")
            
            # Calculate metrics
            avg_latency = np.mean(latencies)
            p95_latency = np.percentile(latencies, 95)
            throughput = 1000 / avg_latency  # QPS
            
            results['avg_latency_ms'].append(avg_latency)
            results['p95_latency_ms'].append(p95_latency)
            results['throughput_qps'].append(throughput)
            
            print(f"📈 Results for {size:,} docs:")
            print(f"   Avg latency: {avg_latency:.1f}ms")
            print(f"   P95 latency: {p95_latency:.1f}ms") 
            print(f"   Throughput: {throughput:.1f} QPS")
            
        finally:
            # Cleanup temporary files
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)
    
    return results

def plot_benchmark_results(results: dict, output_dir: Path):
    """Create visualization of benchmark results"""
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    
    corpus_sizes = results['corpus_sizes']
    
    # Plot 1: Latency vs Corpus Size
    ax1.plot(corpus_sizes, results['avg_latency_ms'], 'o-', label='Average', linewidth=2)
    ax1.plot(corpus_sizes, results['p95_latency_ms'], 's--', label='95th Percentile', linewidth=2)
    ax1.set_xlabel('Corpus Size (documents)')
    ax1.set_ylabel('Latency (ms)')
    ax1.set_title('Query Latency vs Corpus Size')
    ax1.set_xscale('log')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Plot 2: Throughput vs Corpus Size
    ax2.plot(corpus_sizes, results['throughput_qps'], 'o-', color='green', linewidth=2)
    ax2.set_xlabel('Corpus Size (documents)')
    ax2.set_ylabel('Throughput (QPS)')
    ax2.set_title('Query Throughput vs Corpus Size')
    ax2.set_xscale('log')
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Latency Distribution (for largest corpus)
    if len(corpus_sizes) > 0:
        ax3.bar(['Average', 'P95'], 
                [results['avg_latency_ms'][-1], results['p95_latency_ms'][-1]],
                color=['blue', 'orange'])
        ax3.set_ylabel('Latency (ms)')
        ax3.set_title(f'Latency Distribution\n({corpus_sizes[-1]:,} documents)')
        ax3.grid(True, alpha=0.3)
    
    # Plot 4: Performance Summary Table
    ax4.axis('tight')
    ax4.axis('off')
    
    table_data = []
    for i, size in enumerate(corpus_sizes):
        table_data.append([
            f"{size:,}",
            f"{results['avg_latency_ms'][i]:.1f}",
            f"{results['p95_latency_ms'][i]:.1f}",
            f"{results['throughput_qps'][i]:.1f}"
        ])
    
    table = ax4.table(cellText=table_data,
                     colLabels=['Corpus Size', 'Avg Latency (ms)', 'P95 Latency (ms)', 'Throughput (QPS)'],
                     cellLoc='center',
                     loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.5)
    ax4.set_title('Performance Summary', pad=20)
    
    plt.tight_layout()
    
    # Save plot
    plot_path = output_dir / 'retrieval_benchmark.png'
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"📊 Benchmark plot saved to: {plot_path}")
    
    return plot_path

def main():
    parser = argparse.ArgumentParser(description='Benchmark retrieval latency')
    parser.add_argument('--output-dir', type=str, default='benchmarks', 
                       help='Output directory for results')
    parser.add_argument('--corpus-sizes', type=int, nargs='+', 
                       default=[100, 1000, 5000],
                       help='Corpus sizes to benchmark')
    parser.add_argument('--num-queries', type=int, default=10,
                       help='Number of test queries per corpus size')
    
    args = parser.parse_args()
    
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    
    print("🚀 Starting Retrieval Latency Benchmark")
    print(f"📊 Testing corpus sizes: {args.corpus_sizes}")
    print(f"🧪 Queries per size: {args.num_queries}")
    
    # Run benchmark
    results = benchmark_retrieval_latency(args.corpus_sizes, args.num_queries)
    
    # Save results
    results_path = output_dir / 'benchmark_results.json'
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"💾 Results saved to: {results_path}")
    
    # Create visualization
    plot_path = plot_benchmark_results(results, output_dir)
    
    # Print summary
    print("\n🎯 Benchmark Summary:")
    for i, size in enumerate(results['corpus_sizes']):
        print(f"  {size:,} docs: {results['avg_latency_ms'][i]:.1f}ms avg, "
              f"{results['throughput_qps'][i]:.1f} QPS")
    
    print(f"\n✅ Benchmark complete! Results in {output_dir}")

if __name__ == "__main__":
    main()
