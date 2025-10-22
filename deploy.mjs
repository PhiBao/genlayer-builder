#!/usr/bin/env node

import { readFileSync, writeFileSync } from 'fs';
import { resolve } from 'path';
import { createClient, createAccount } from 'genlayer-js';
import { localnet } from 'genlayer-js/chains';
import { TransactionStatus } from 'genlayer-js/types';

// Use GenLayer Studio Network (better for development/testing)
const studioNetwork = {
  ...localnet,
  id: 61999,
  name: "GenLayer Studio",
  rpcUrls: {
    default: {
      http: ["https://studio.genlayer.com/api"]
    }
  },
  blockExplorers: {
    default: {
      name: "GenLayer Studio",
      url: "https://studio.genlayer.com"
    }
  }
};

async function deployToTestnet() {
  try {
    console.log('🚀 GenLayer Prediction Market Deployment');
    console.log('=========================================\n');
    
    // Get private key from environment
    const privateKey = process.env.GENLAYER_PRIVATE_KEY;
    if (!privateKey) {
      throw new Error('❌ GENLAYER_PRIVATE_KEY environment variable not set');
    }
    
    // Create account from private key
    console.log('🔑 Creating account from private key...');
    const account = createAccount(`0x${privateKey}`);
    console.log(`   Address: ${account.address}\n`);
    
    // Create client for testnet
    console.log('🌐 Connecting to GenLayer Studio...');
    const client = createClient({
      chain: studioNetwork,
      account: account,
      endpoint: "https://studio.genlayer.com/api"
    });
    console.log(`   Network: ${studioNetwork.name}`);
    console.log(`   Chain ID: ${studioNetwork.id}`);
    console.log(`   RPC: https://studio.genlayer.com/api\n`);
    
    // Read contract code
    const contractPath = resolve(process.cwd(), 'contracts/prediction_market.py');
    console.log('📄 Reading production contract file...');
    console.log(`   Path: ${contractPath}`);
    const contractCode = new Uint8Array(readFileSync(contractPath));
    console.log(`   Size: ${contractCode.length} bytes\n`);
    
    // Initialize consensus
    console.log('⚙️  Initializing consensus smart contract...');
    await client.initializeConsensusSmartContract();
    console.log('   ✓ Consensus initialized\n');
    
    // Deploy contract
    console.log('📦 Deploying production Prediction Market contract...');
    const deployTx = await client.deployContract({
      code: contractCode,
      args: [], // No constructor args needed for the full contract
    });
    
    console.log(`   Transaction Hash: ${deployTx}`);
    console.log('   ⏳ Waiting for confirmation (this may take 1-2 minutes)...');
    console.log('   💡 You can check status at:');
    console.log(`      https://studio.genlayer.com\n`);

    // Wait for receipt (GenLayer transactions can take 60-120 seconds to finalize)
    let receipt;
    try {
      // Try waiting for FINALIZED first (preferred final state)
      receipt = await client.waitForTransactionReceipt({
        hash: deployTx,
        status: TransactionStatus.FINALIZED,
        retries: 600, // ~10 minutes max wait
      });
    } catch (finalizedErr) {
      console.log('   ℹ️  Not yet finalized, checking for ACCEPTED status...');
      try {
        // Fall back to ACCEPTED status
        receipt = await client.waitForTransactionReceipt({
          hash: deployTx,
          status: TransactionStatus.ACCEPTED,
          retries: 100,
        });
      } catch (acceptedErr) {
        // If both failed, try to capture receipt info
        console.error('\n⚠️  Transaction not ACCEPTED or FINALIZED within timeout. Capturing info...');
        try {
          if (typeof client.getTransactionReceipt === 'function') {
            const r = await client.getTransactionReceipt({ hash: deployTx });
            receipt = r || null;
          }
        } catch (innerErr) {
          console.error('   Could not fetch receipt:', innerErr?.message || innerErr);
        }
        
        // Save error and receipt to disk
        receipt = receipt || { txHash: deployTx, note: 'no receipt available (timed out)' };
        try {
          writeFileSync(resolve(process.cwd(), 'tx_receipt.json'), 
            JSON.stringify({ error: String(acceptedErr), receipt }, null, 2));
          console.log('   Saved receipt snapshot to tx_receipt.json');
        } catch (fsErr) {
          console.error('   Failed to write tx_receipt.json:', fsErr?.message || fsErr);
        }

        console.error('\n❌ Deployment likely failed or stuck. See tx_receipt.json for details.');
        console.error('   Studio:', `https://studio.genlayer.com`);
        throw acceptedErr;
      }
    }

    console.log('📋 Transaction Receipt:');
    console.log(`   Status: ${receipt.statusName}`);

    // Check deployment status
    if (receipt.statusName !== TransactionStatus.ACCEPTED && 
        receipt.statusName !== TransactionStatus.FINALIZED) {
      console.error('\n❌ Deployment failed or transaction not accepted');
      // save receipt for analysis
      try {
        writeFileSync(resolve(process.cwd(), 'tx_receipt.json'), JSON.stringify(receipt, null, 2));
        console.log('   Saved full receipt to tx_receipt.json for debugging');
      } catch (fsErr) {
        console.error('   Failed to write tx_receipt.json:', fsErr?.message || fsErr);
      }
      console.error('Receipt (short):', JSON.stringify(receipt, null, 2));
      console.error('Studio:', `https://studio.genlayer.com`);
      throw new Error('Transaction not accepted');
    }
    
    // Get contract address
    const contractAddress = receipt.data?.contract_address || 
                           receipt.txDataDecoded?.contractAddress;
    
    console.log(`   Contract Address: ${contractAddress}\n`);
    
    // Save deployment info
    const deploymentInfo = {
      network: 'studio',
      chainId: studioNetwork.id,
      contractAddress: contractAddress,
      deployer: account.address,
      transactionHash: deployTx,
      deployedAt: new Date().toISOString(),
      studioUrl: `https://studio.genlayer.com`,
      txUrl: `https://studio.genlayer.com`
    };
    
    const outputPath = resolve(process.cwd(), 'deployed_contract.json');
    writeFileSync(outputPath, JSON.stringify(deploymentInfo, null, 2));
    
    // Print success message
    console.log('✅ DEPLOYMENT SUCCESSFUL!\n');
    console.log('📍 Contract Details:');
    console.log(`   Address: ${contractAddress}`);
    console.log(`   Deployer: ${account.address}`);
    console.log(`   Network: ${studioNetwork.name}`);
    console.log(`   Chain ID: ${studioNetwork.id}\n`);
    console.log('🔗 Links:');
    console.log(`   Studio: ${deploymentInfo.studioUrl}\n`);
    console.log(`💾 Deployment info saved to: ${outputPath}\n`);
    
    return contractAddress;
    
  } catch (error) {
    console.error('\n💥 DEPLOYMENT FAILED\n');
    console.error('Error:', error.message);
    if (error.stack) {
      console.error('\nStack trace:');
      console.error(error.stack);
    }
    process.exit(1);
  }
}

// Run deployment
console.log('\n');
deployToTestnet()
  .then((address) => {
    console.log('🎉 All done! Contract deployed at:', address);
    process.exit(0);
  })
  .catch((error) => {
    console.error('Fatal error:', error);
    process.exit(1);
  });
